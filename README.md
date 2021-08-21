# Write Message
POST https://guarded-brushlands-59478.herokuapp.com/api/messages/

body: 
{
  "sender": 1,
  "receiver": 1,
  "subject": "subject example",
  "message": "message example"
}

# Get all messages for a specific user 
GET https://guarded-brushlands-59478.herokuapp.com/api/users/<user_id>/messages/

# Get all unread messages for a specific user
GET https://guarded-brushlands-59478.herokuapp.com/api/users/<user_id>/messages/?seen=False

# Read message (return one message)
GET https://guarded-brushlands-59478.herokuapp.com/api/messages/<message_id>/

# Delete message (as owner or as receiver)
DELETE https://guarded-brushlands-59478.herokuapp.com/api/messages/<message_id>/

# Login url
POST https://guarded-brushlands-59478.herokuapp.com/api/accounts/login/

{
  "username": "username",
  "password": "password"
}

# logout url
POST https://guarded-brushlands-59478.herokuapp.com/api/accounts/logout/

