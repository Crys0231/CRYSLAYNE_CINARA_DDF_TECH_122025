import pathlib
import os
import pandas as pd


# Caminhos base 

if "__file__" in globals():
    BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
else:
    # Notebook: assume que você está na raiz do projeto
    BASE_DIR = pathlib.Path(os.getcwd()).resolve()

TRUSTED_DIR = BASE_DIR / "data" / "trusted"
REFINED_DIR = BASE_DIR / "data" / "refined"


# ==============================
#   TESTES - CAMADA TRUSTED
# ==============================


def test_trusted_files_exist():
    """Verifica se todos os arquivos da camada trusted existem."""
    expected_files = [
        TRUSTED_DIR / "products_trusted.parquet",
        TRUSTED_DIR / "customers_trusted.parquet",
        TRUSTED_DIR / "sales_trusted.parquet",
    ]

    for path in expected_files:
        assert path.exists(), f"Arquivo esperado não encontrado: {path}"


def test_products_trusted_schema_and_quality():
    """Valida schema e regras de negócio da tabela products_trusted."""
    df = pd.read_parquet(TRUSTED_DIR / "products_trusted.parquet")

    # 1) Quantidade de linhas
    assert len(df) == 10_000, "products_trusted deve ter exatamente 10.000 registros"

    # 2) Colunas obrigatórias
    required_cols = [
        "product_id",
        "product_name",
        "bearing_type",
        "material",
        "manufacturer",
        "model",
        "load_capacity",
        "max_speed",
        "temperature_limit",
        "unit_cost",
        "list_price",
        "problem_type",
        "technical_description",
        "technical_features",
        "llm_product_description",
    ]
    for col in required_cols:
        assert col in df.columns, f"Coluna obrigatória ausente em products_trusted: {col}"

    # 3) Sem valores nulos (como garantido nas transformações)
    assert df.isnull().sum().sum() == 0, "products_trusted não deve ter valores nulos"

    # 4) Regra crítica: margem positiva (unit_cost < list_price)
    assert (df["unit_cost"] < df["list_price"]).all(), (
        "Ainda existem produtos com unit_cost >= list_price em products_trusted!"
    )


def test_customers_trusted_schema_and_quality():
    """Valida schema e integridade da tabela customers_trusted."""
    df = pd.read_parquet(TRUSTED_DIR / "customers_trusted.parquet")

    # 1) Quantidade de linhas
    assert len(df) == 5_000, "customers_trusted deve ter exatamente 5.000 registros"

    # 2) Colunas obrigatórias
    required_cols = [
        "customer_id",
        "company_name",
        "industry",
        "company_size",
        "country",
        "relationship_start_date",
        "last_updated",
        "annual_revenue_estimated",
        "maintenance_budget_annual",
        "downtime_cost_per_hour",
        "expected_problems",
    ]
    for col in required_cols:
        assert col in df.columns, f"Coluna obrigatória ausente em customers_trusted: {col}"

    # 3) Sem valores nulos
    assert df.isnull().sum().sum() == 0, "customers_trusted não deve ter valores nulos"

    # 4) expected_problems deve variar entre os clientes (não pode ser tudo igual)
    expected_problems_str = df["expected_problems"].apply(lambda x: str(sorted(x)))

    unique_count = expected_problems_str.nunique()

    assert unique_count > 1, (
        f"expected_problems deve variar entre clientes. "
        f"Encontrados apenas {unique_count} padrão(ões) único(s)."
    )




def test_sales_trusted_schema_and_quality():
    """Valida schema e integridade da tabela sales_trusted."""
    df = pd.read_parquet(TRUSTED_DIR / "sales_trusted.parquet")

    # 1) Quantidade de linhas
    assert len(df) == 120_000, "sales_trusted deve ter exatamente 120.000 registros"

    # 2) Colunas obrigatórias
    required_cols = [
        "sale_id",
        "customer_id",
        "product_id",
        "sale_date",
        "last_updated",
        "quantity",
        "unit_price",
        "total_price",
        "discount_percentage",
        "payment_terms",
        "sales_channel"
    ]
    for col in required_cols:
        assert col in df.columns, f"Coluna obrigatória ausente em sales_trusted: {col}"

    # 3) Sem valores nulos
    assert df.isnull().sum().sum() == 0, "sales_trusted não deve ter valores nulos"

    # 4) Quantidade e preços positivos
    assert (df["quantity"] > 0).all(), "sales_trusted.quantity deve ser > 0"
    assert (df["unit_price"] > 0).all(), "sales_trusted.unit_price deve ser > 0"
    assert (df["total_price"] > 0).all(), "sales_trusted.total_price deve ser > 0"

    # 5) Validação do cálculo de total_price (com tolerância)
    tolerance = 0.01
    diffs = (df["total_price"] - (df["quantity"] * df["unit_price"])).abs()
    assert (diffs <= tolerance).all(), "total_price inconsistente para algumas vendas"


# ==============================
#   TESTES - CAMADA REFINED
# ==============================


def test_products_features_schema():
    """Valida schema da tabela de features de produtos (para ML)."""
    df = pd.read_parquet(REFINED_DIR / "dim_products.parquet")

    assert len(df) == 10_000, "dim_products deve ter 10.000 registros"

    required_cols = [
        "product_id",
        "product_name",
        "bearing_type",
        "material",
        "problem_type",
        "technical_description",
        "technical_features",
        "full_description",
    ]
    for col in required_cols:
        assert col in df.columns, f"Coluna obrigatória ausente em products_features: {col}"

    # Campo que será usado no modelo de similaridade
    assert df["full_description"].notnull().all(), "full_description não pode ter nulos"


def test_customers_features_schema():
    """Valida schema da tabela de features de clientes (para ML)."""
    df = pd.read_parquet(REFINED_DIR / "dim_customers.parquet")

    assert len(df) == 5_000, "dim_customers deve ter 5.000 registros"

    required_cols = [
        "customer_id",
        "industry",
        "company_size",
        "maintenance_model",
        "equipment_criticality",
        "expected_problems",
    ]
    for col in required_cols:
        assert col in df.columns, f"Coluna obrigatória ausente em customers_features: {col}"

    assert df.isnull().sum().sum() == 0, "customers_features não deve ter valores nulos"


def test_sales_trusted_foreign_keys_consistency():
    """Valida integridade referencial básica entre sales_trusted, customers_trusted e products_trusted."""
    sales = pd.read_parquet(TRUSTED_DIR / "sales_trusted.parquet")
    customers = pd.read_parquet(TRUSTED_DIR / "customers_trusted.parquet")
    products = pd.read_parquet(TRUSTED_DIR / "products_trusted.parquet")

    # FK: customer_id
    invalid_customers = ~sales["customer_id"].isin(customers["customer_id"])
    assert not invalid_customers.any(), "Existem registros em sales_trusted com customer_id inválido"

    # FK: product_id
    invalid_products = ~sales["product_id"].isin(products["product_id"])
    assert not invalid_products.any(), "Existem registros em sales_trusted com product_id inválido"
