import graphene
import json
from datetime import datetime

class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()

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
schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
      {
          users {
                id
                username
                createdAt
          }
      }
    '''
)

dicResult  = dict(result.data.items())
print(json.dumps(dicResult, indent=2))