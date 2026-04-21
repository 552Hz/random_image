"""
随机图片插件
功能：当有人发送 /随机拍切姿势 时，从 data 目录随机发送一张图片
"""

import random
from pathlib import Path

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import AstrBotConfig, logger
from astrbot.api.message_components import Image as ImageSeg


class RandomImagePlugin(Star):
    """随机图片插件"""

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.name = "随机图片"

        # 获取插件目录下的 data 文件夹
        plugin_dir = Path(__file__).parent
        self.data_dir = plugin_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        logger.info("随机图片插件已加载")

    def _get_random_image(self) -> Path | None:
        """从 data 目录随机获取一张图片"""
        if not self.data_dir.exists():
            logger.error(f"data 目录不存在: {self.data_dir}")
            return None

        # 获取所有图片文件
        extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}
        images = [
            f for f in self.data_dir.iterdir()
            if f.is_file() and f.suffix.lower() in extensions
        ]

        if not images:
            logger.warning(f"data 目录没有图片: {self.data_dir}")
            return None

        return random.choice(images)

    @filter.command("随机拍切姿势")
    async def random_image(self, event: AstrMessageEvent):
        """随机发送一张图片"""
        image_path = self._get_random_image()

        if not image_path:
            yield event.plain_result("❌ 未找到图片，请先将图片放入 data 目录")
            return

        try:
            # 发送图片
            yield event.image_result(str(image_path))
        except Exception as e:
            logger.error(f"发送图片失败: {e}")
            yield event.plain_result(f"❌ 发送图片失败: {str(e)}")
