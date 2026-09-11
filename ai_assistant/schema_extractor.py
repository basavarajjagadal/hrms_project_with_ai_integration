
from django.apps import apps


from langchain_core.documents import Document

def get_sample_data(model):
    """
    Fetch 1-2 sample records with all field values
    """
    try:
        records = model.objects.all()[:2]

        samples = []

        for obj in records:
            field_data = []

            for field in model._meta.fields:
                value = getattr(obj, field.name)

                # Handle foreign keys (show readable value)
                if field.is_relation and value:
                    value = str(value)

                field_data.append(f"{field.name}: {value}")

            samples.append(", ".join(field_data))

        return samples

    except Exception:
        return []



def extract_schema_documents():
    documents = []

    for model in apps.get_models():

        # Skip Django internal apps
        if model._meta.app_label in [
            "admin",
            "auth",
            "contenttypes",
            "sessions"
        ]:
            continue

        model_name = model.__name__
        table_name=model._meta.db_table

        columns = []
        relationships = []
        choices_info = []

        for field in model._meta.get_fields():

            # Skip reverse relations
            if field.auto_created and not field.concrete:
                continue

            # Handle relationships
            if field.is_relation:

                if field.many_to_one:
                    relationships.append(
                        f"{field.name}_id (ForeignKey → {field.related_model._meta.db_table})"
                    )

                elif field.one_to_one:
                    relationships.append(
                        f"{field.name}_id (OneToOne → {field.related_model._meta.db_table})"
                    )

                elif field.many_to_many:
                    relationships.append(
                        f"{field.name} (ManyToMany → {field.related_model._meta.db_table})"
                    )

            else:
                columns.append(
                    f"{field.name} ({field.get_internal_type()})"
                )

                # Handle choices (VERY IMPORTANT)
                if hasattr(field, "choices") and field.choices:
                    choices = [choice[0] for choice in field.choices]
                    choices_info.append(
                        f"{field.name} possible values: {choices}"
                    )

        # Get sample records
        samples = get_sample_data(model)

        schema_text = f"""
Model: {model_name}
Table: {table_name}

Columns:
{', '.join(columns) if columns else 'None'}

Relationships:
{', '.join(relationships) if relationships else 'None'}

Choices:
{', '.join(choices_info) if choices_info else 'None'}

Example Records:
{', '.join(samples) if samples else 'None'}
"""

        documents.append(
            Document(page_content=schema_text.strip())
        )

    return documents