import graphene

TENIS = [
    {'id': '1', 'nombre': 'Tenis1', 'precio': 1500, 'stock': 5, 'disponible': True},
    {'id': '2', 'nombre': 'Tenis2', 'precio': 200, 'stock': 3, 'disponible': True},
    {'id': '3', 'nombre': 'Tenis3', 'precio': 50, 'stock': 10, 'disponible': True},
]

class TenisType(graphene.ObjectType):
    id = graphene.ID()
    nombre = graphene.String()
    precio = graphene.Float()
    stock = graphene.Int()
    disponible = graphene.Boolean()

class UpdateStock(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        amount = graphene.Int(required=True)

    tenis = graphene.Field(TenisType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, amount):
        tenis = next((e for e in TENIS if e['id'] == id), None)
        if not tenis:
            return UpdateStock(success=False, message="Producto no encontrado")

        tenis['stock'] += amount

        if tenis['stock'] < 0:
            tenis['stock'] = 0

        tenis['disponible'] = tenis['stock'] > 0

        return UpdateStock(
            tenis=tenis,
            success=True,
            message="Stock actualizado correctamente"
        )

class Mutation(graphene.ObjectType):
    update_stock = UpdateStock.Field()

class Query(graphene.ObjectType):
    tenis = graphene.List(TenisType)

    def resolve_tenis(parent, info):
        return TENIS

schema = graphene.Schema(query=Query, mutation=Mutation)
