from smart_rh.firebase.FirebaseAPI import FirebaseAPI

DATABASE_SECRET = "2Ah8BmXrPZCasGX1BX0BxwomYSbE6WU4TrHLynhi"
DATABASE_URL = "https://smartrh-2025-46b3c-default-rtdb.firebaseio.com/"

firebase = FirebaseAPI(database_url=DATABASE_URL, secret_key=DATABASE_SECRET)
