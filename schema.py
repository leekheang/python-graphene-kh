import graphene
import uuid
import json
from datetime import datetime

class User(graphene.ObjectType):
    id = graphene.ID(default_value=uuid.uuid4())
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())


class Query(graphene.ObjectType):
    users = graphene.List(User , limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "hello"
    
    def resolve_is_admin(self, info):
        return True
    
    def resolve_users(self, info , limit=None):
        return [
            User( id="1", username="leekheang", created_at=datetime.now()),
            User( id="2", username="nat", created_at=datetime.now())
        ][:limit]

class Create_User(graphene.Mutation):
    user = graphene.Field(User)
    
    class Arguments:
        username = graphene.String()
    
    def mutate(self, info ,username):
        user = User(username=username)
        return Create_User(user=user)

class Mutation(graphene.ObjectType):
    create_user = Create_User.Field()



schema = graphene.Schema(query=Query , mutation=Mutation)

result = schema.execute(
    '''
        mutation {
            createUser(username:  "yong"){
               user {
                    id
                    username
                    createdAt
               }
            }
        }
    '''
)

dicResult  = dict(result.data.items())
print(json.dumps(dicResult, indent=2))