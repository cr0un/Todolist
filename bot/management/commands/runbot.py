from django.core.management import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory
from goals.serializers import GoalSerializer


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.user_sessions = {}

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                if item.message:
                    self.handle_message(item.message)
                elif item.my_chat_member:
                    self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)

        if tg_user.user:
            self.handle_authorized_user(tg_user, msg)
        else:
            self.handle_unauthorized_user(tg_user, msg)

    def handle_authorized_user(self, tg_user: TgUser, msg: Message):
        session_data = self.user_sessions.get(tg_user.chat_id, {})

        if msg.text == '/goals':
            user = tg_user.user
            goals = Goal.objects.filter(
                is_deleted=False,
                category__is_deleted=False,
                category__board__participants__user=user
            )

            serialized_goals = GoalSerializer(goals, many=True)
            goals_text = ""

            for idx, goal in enumerate(serialized_goals.data, start=1):
                goals_text += f"{idx}. {goal['title']}\n"

            if goals_text:
                self.tg_client.send_message(chat_id=tg_user.chat_id, text=goals_text)
            else:
                self.tg_client.send_message(chat_id=tg_user.chat_id, text="У вас нет активных целей.")

        elif msg.text == '/create':
            session_data["creating_goal"] = True
            self.user_sessions[tg_user.chat_id] = session_data
            self.tg_client.send_message(chat_id=tg_user.chat_id, text="Введите ID категории:")
            self.send_goal_categories(tg_user)

        elif session_data.get("creating_goal"):
            if session_data.get("category_id"):
                goal_title = msg.text
                category_id = session_data["category_id"]
                self.create_goal(tg_user, category_id, goal_title)
                del session_data["creating_goal"]
                del session_data["category_id"]
                self.tg_client.send_message(chat_id=tg_user.chat_id, text=f"Цель '{goal_title}' создана.")
            else:
                category_id = msg.text
                if self.is_valid_category_id(tg_user, category_id):
                    session_data["category_id"] = category_id
                    self.user_sessions[tg_user.chat_id] = session_data
                    self.tg_client.send_message(chat_id=tg_user.chat_id, text="Введите название цели:")
                else:
                    self.tg_client.send_message(
                        chat_id=tg_user.chat_id,
                        text="Неверный ID категории. Введите ID категории снова:"
                    )

    def send_goal_categories(self, tg_user: TgUser):
        user = tg_user.user
        categories = GoalCategory.objects.filter(is_deleted=False, board__participants__user=user)

        if not categories:
            self.tg_client.send_message(chat_id=tg_user.chat_id, text="У вас нет доступных категорий.")
            return

        categories_text = "Выберите категорию, введя ее ID:\n"
        for category in categories:
            categories_text += f"{category.id}. {category.title}\n"

        self.tg_client.send_message(chat_id=tg_user.chat_id, text=categories_text)

    def handle_unauthorized_user(self, tg_user: TgUser, msg: Message):
        code = tg_user.generate_verification_code()
        tg_user.verification_code = code
        tg_user.save()

        self.tg_client.send_message(chat_id=msg.chat.id, text=f'Привет! Код верификации: {code}')

    def is_valid_category_id(self, tg_user: TgUser, category_id: str) -> bool:
        try:
            category_id = int(category_id)
        except ValueError:
            return False

        user = tg_user.user
        return GoalCategory.objects.filter(
            id=category_id,
            is_deleted=False,
            board__participants__user=user
        ).exists()

    def create_goal(self, tg_user: TgUser, category_id: int, goal_title: str):
        user = tg_user.user
        category = GoalCategory.objects.get(id=category_id)
        Goal.objects.create(user=user, category=category, title=goal_title)

