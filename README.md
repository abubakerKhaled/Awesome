# AWESOME Web App

A social photo-sharing web application built with Django and HTMX for dynamic interactions. Users can create accounts, share photos, and interact with posts through comments and replies.

## Features

- **User Accounts:** Create and manage user profiles.
- **Photo Sharing:** Upload and share photos with customizable posts.
- **Comments & Replies:** Engage with posts through comments and nested replies.
- **Messaging:** Send and receive encrypted messages between users.

## Technologies

- **Django:** Framework for server-side logic and database management.
- **HTMX:** Enhances user interactions with dynamic updates without full page reloads.
- **Cryptography:** Used for encrypting and decrypting messages.

## Models

### a_posts App

- **Tag**
  - Categorizes posts.
  - Fields: `name`, `image`, `slug`, `order`.
  - Meta: Ordered by `order`.

- **Post**
  - Represents a photo post.
  - Fields: `title`, `artist`, `url`, `author`, `image`, `body`, `likes`, `tags`, `created`, `id`.
  - Meta: Ordered by creation date.

- **LikedPost**
  - Tracks which users liked which posts.
  - Fields: `user`, `post`, `created_at`.

- **Comment**
  - Represents a comment on a post.
  - Fields: `author`, `parent_post`, `body`, `likes`, `created_at`, `id`.
  - Meta: Ordered by creation date.

- **LikedComment**
  - Tracks which users liked which comments.
  - Fields: `user`, `comment`, `created_at`.

- **Reply**
  - Represents a reply to a comment.
  - Fields: `author`, `parent_comment`, `body`, `likes`, `created_at`, `id`.
  - Meta: Ordered by creation date.

- **LikedReply**
  - Tracks which users liked which replies.
  - Fields: `user`, `reply`, `created_at`.

### a_users App

- **Profile**
  - Extends the default `User` model with additional details.
  - Fields: `user`, `realname`, `image`, `email`, `location`, `bio`, `created`, `gender`.
  - Methods: 
    - `__str__()`: Returns the user associated with the profile.
    - `avatar`: Returns the URL of the profile image or a default image.
    - `name`: Returns the real name or username.

### a_inbox App

- **InboxMessage**
  - Represents a message sent between users.
  - Fields: `sender`, `Conversation`, `body`, `created_at`.
  - Methods:
    - `body_decrypted`: Decrypts the message body.
  - Meta: Ordered by creation date.

- **Conversation**
  - Represents a conversation between users.
  - Fields: `id`, `participants`, `lastmessage_created`, `is_seen`.
  - Meta: Ordered by last message creation date.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the app at `http://localhost:8000`.

## Configuration

- **Encryption Key:** Set `ENCRYPT_KEY` in your Django settings to ensure secure message encryption.
