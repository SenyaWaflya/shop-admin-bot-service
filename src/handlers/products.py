from io import BytesIO

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.file_storage.files import FilesApi
from src.api.shop_backend.products import ProductsApi
from src.states import AddProduct

products_router = Router(name='products')
fields_need = 4


@products_router.message(F.text == 'Добавить товар')
async def add_product_instruction(message: Message, state: FSMContext) -> None:
    await state.set_state(AddProduct.data)
    await message.answer(
        text=(
            'Введите следующие данные: <b>фирма телефона, модель (включая цвет и объём памяти), цену, '
            'количество на складе</b>. '
            'Пример: \n'
            'Apple\niPhone 16 Black (128gb)\n60000\n16'
        ),
    )

@products_router.message(AddProduct.data)
async def add_product_data(message: Message, state: FSMContext) -> None:
    fields = message.text.split('\n')
    if len(fields) != fields_need:
        await message.answer(text='Неверный формат. Нужно 4 строки.')
        return

    brand, title, price, quantity = fields

    if not price.isdigit() or not quantity.isdigit():
        await message.answer(text='Цена и количество должны быть числами.')
        return

    price = int(price)
    quantity = int(quantity)

    await state.update_data(
        brand=brand,
        title=title,
        price=price,
        quantity=quantity,
    )

    await message.answer(text='Теперь загрузите фото')
    await state.set_state(AddProduct.image)

@products_router.message(AddProduct.image, F.photo)
async def add_product(message: Message, state: FSMContext, bot: Bot) -> None:
    photo = message.photo[-1]
    file = await bot.get_file(file_id=photo.file_id)
    buffer = BytesIO()
    await bot.download_file(file_path=file.file_path, destination=buffer)
    image_bytes = buffer.getvalue()
    product_data = await state.get_data()
    image_s3_path = await FilesApi.upload(image_bytes, str(bot.id), str(message.from_user.id))
    product_data['image_path'] = image_s3_path.file_path


    await ProductsApi.create(product_data)
    await message.answer(text=(
        'Телефон был добавлен в каталог\n'
        f'Фирма: {product_data['brand']}\n'
        f'Модель: {product_data['title']}\n'
        f'Цена: {product_data['price']}\n'
        f'Количество на складе: {product_data['quantity']}'
    ))

@products_router.message(AddProduct.image)
async def wrong_image(message: Message) -> None:
    await message.answer(text='Пожалуйста, отправьте именно фото товара.')
