import graphene
import uuid
import json
from datetime import datetime

class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()
    
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

class CreateUser(graphene.Mutation):
    user = graphene.Field(User)
    
    class Arguments:
        username = graphene.String()
    
    def mutate(self, info ,username):
        user = User(username=username)
        return CreateUser(user=user)

class CreatePost(graphene.Mutation):

    post = graphene.Field(Post)
    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content ):
        if info.context.get('is_anonymous'):
            raise Exception("Not Authenticated")
        post = Post(title=title, content=content)
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()



schema = graphene.Schema(query=Query , mutation=Mutation)

result = schema.execute(

    '''    
        # mutation ($username : String) {
        #     createUser(username: $username){
        #        user {
        #             id
        #             username
        #             createdAt
        #        }
        #     }
        # }

        mutation {
            createPost(title: "herry Poter", content: "google.com"){
                post{
                    title
                    content
                }
            }
        }

        # query getUsersQuery($limit : Int) {
        #     users(limit: $limit){         
        #         id
        #         username
        #         createdAt
        #     }
        # }
        
    ''',
    # variable_values={'limit': 2}
    # variable_values={'username': 'yong'}
    context = { 'is_anonymous': True }
)

dicResult  = dict(result.data.items())
print(json.dumps(dicResult, indent=2))