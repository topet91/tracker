from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col


def get_product_category_pairs(
        products_df: DataFrame,
        categories_df: DataFrame,
        product_category_links_df: DataFrame
) -> DataFrame:
    """
    Возвращает DataFrame с парами "Продукт-Категория" и продуктами без категорий.

    :param products_df: Датафрейм с колонками ['product_id', 'product_name']
    :param categories_df: Датафрейм с колонками ['category_id', 'category_name']
    :param product_category_links_df: Датафрейм связей ['product_id', 'category_id']
    :return: Датафрейм с колонками ['product_name', 'category_name']
    """
    # Объединяем продукты с их категориями
    product_with_categories = products_df.alias("p").join(
        product_category_links_df.alias("pc"),
        col("p.product_id") == col("pc.product_id"),
        "left"
    ).join(
        categories_df.alias("c"),
        col("pc.category_id") == col("c.category_id"),
        "left"
    )

    # Выбираем нужные колонки и добавляем продукты без категорий
    result = product_with_categories.select(
        col("p.product_name").alias("product_name"),
        col("c.category_name").alias("category_name")
    ).distinct()

    return result


if __name__ == "__main__":
    # Инициализируем SparkSession
    spark = SparkSession.builder \
        .appName("ProductCategoryPairs") \
        .getOrCreate()

    # Создаем тестовые данные
    products = spark.createDataFrame(
        [(1, "Молоко"), (2, "Телевизор"), (3, "Книга")],
        ["product_id", "product_name"]
    )

    categories = spark.createDataFrame(
        [(101, "Молочные продукты"), (102, "Электроника")],
        ["category_id", "category_name"]
    )

    links = spark.createDataFrame(
        [(1, 101), (2, 102)],
        ["product_id", "category_id"]
    )

    # Вызываем метод
    result = get_product_category_pairs(products, categories, links)
    result.show()