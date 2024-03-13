from django_graphbox.builder import SchemaBuilder
from .models import Category, User, Role, Address, AddressType, State, Country, SubCategory, Color, Product

builder = SchemaBuilder()
builder.add_model(User)
builder.add_model(Category)
builder.add_model(Role)
builder.add_model(Address)
builder.add_model(AddressType)
builder.add_model(State)
builder.add_model(Country)
builder.add_model(SubCategory)
builder.add_model(Color)
builder.add_model(Product)


query_class = builder.build_schema_query()
mutation_class = builder.build_schema_mutation()