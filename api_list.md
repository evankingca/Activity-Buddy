GymGolf API Endpoints
Authentication & User Accounts

    POST /auth/signup/ — create a new user

    POST /auth/login/ — authenticate user

    POST /auth/logout/ — end session

    POST /auth/password-reset/ — request password reset

    POST /auth/password-reset/confirm/ — confirm password reset

    GET /auth/me/ — get current authenticated user

    PATCH /auth/me/ — update current user profile

Users

    GET /users/ — list all users

    GET /users/{id}/ — view a user profile

    PATCH /users/{id}/ — edit user profile (self only)

    GET /users/{id}/activities/ — list user’s activities

    GET /users/{id}/preferences/ — list user’s preferences

Activities

    GET /activities/ — list all activities

    GET /activities/{id}/ — get activity details

    POST /activities/ — create activity (admin only)

    PATCH /activities/{id}/ — update activity (admin only)

    DELETE /activities/{id}/ — delete activity (admin only)

User Activities

    POST /user-activities/ — add an activity to a user

    PATCH /user-activities/{id}/ — update user activity

    DELETE /user-activities/{id}/ — remove user activity

Preferences

    GET /preferences/ — list all preference entries

    POST /preferences/ — create a preference

    PATCH /preferences/{id}/ — update a preference

    DELETE /preferences/{id}/ — delete a preference

Connections (Buddy System + Blocking)

    GET /connections/ — list current user’s connections

    POST /connections/ — send a buddy request

    PATCH /connections/{id}/accept/ — accept request

    PATCH /connections/{id}/reject/ — reject request

    PATCH /connections/{id}/block/ — block user

    PATCH /connections/{id}/unblock/ — unblock user

Messaging

    GET /connections/{id}/messages/ — list all messages in this connection

    POST /connections/{id}/messages/send/ — send a message in this connection

    GET /messages/{id}/ — get a single message