Create script to prepare simple table with embeddings.
- Input is ../source_json/producers.json
- Create Pandas frame
- Table columns should be producerName, productName, productDescription and productId
- Create new column combinedText in format PRODUCER: name, PRODUCT: name, DESCRIPTION: description
- Call OpenAI embeddings model large to get embeddings into column called embedding, but cap it to 2000 dimensions.
- Important note - due to pgvector indexing limitations we want to keep the dimensionality of the embeddings to 2000.
- Use envs as in template provided
- LLM can be rate limited, implement retries and note model will typically return amount of seconds to wait during 429 errors.
- Report progress ever 100 records or so
- Once done export this as Parquet file ../processed/simple_products.parquet
- Frameworks log level should be set to WARNING while keeping your own logger at INFO level

Here is .env.template for your reference
<env.template>
# Unified OpenAI configuration (works for OpenAI and Azure OpenAI)
# Required
OPENAI_API_KEY=sk-your-openai-or-azure-key
OPENAI_MODEL=gpt-5
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

# Optional (required for Azure)
OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/v1/
OPENAI_API_VERSION=preview

# PostgreSQL Database Configuration (standard PG environment variables)
PGHOST=localhost
PGPORT=5432
PGDATABASE=aidb
PGUSER=admin
PGPASSWORD=my-secure-password-here
</env.template>
