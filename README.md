# Harvard Social Network Project  

## Overview  

This project is an interactive social networking platform where users can register, log in, create posts, follow others, and engage with real-time interactions. Designed with a responsive interface, the platform ensures smooth navigation and an engaging user experience.  

## Features  

- **User Authentication:** Register and log in securely.  
- **Post Creation & Editing:** Users can publish posts and edit them instantly.  
- **Profile Management:** Personal profile page with user info, profile image, and follower/following count.  
- **Follow System:** Follow/unfollow users and view a curated Following feed.  
- **Pagination:** Browse all posts with an optimized page navigation system.  
- **Live Interactions:** Like/unlike posts with live count updates, and add comments & replies.  
- **Responsive UI:** Built with Bootstrap for seamless access across devices.  
- **Testing & Admin Panel:** Unit tests and admin configurations ensure reliability.  

## Tech Stack  

- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Backend:** Django (Python)  
- **Database:** PostgreSQL / SQLite  
- **Authentication:** Django Auth System  
- **Testing:** Django Test Framework  

## Installation & Setup  

1. Clone the repository:  
   

  ``` git clone https://github.com/yourusername/harvard-social-network.git
   cd harvard-social-network```
  
2. Create a virtual environment and install dependencies:  
   
```
   python -m venv venv  
   source venv/bin/activate  # (On Windows use venv\Scripts\activate)  
   pip install -r requirements.txt  
   ```
  
3. Run migrations and start the server:  
   
```
   python manage.py migrate  
   python manage.py runserver 
   ```
  
4. Access the project in your browser at `http://127.0.0.1:8000/`.  

## Contributing  

Feel free to fork the repository, submit pull requests, or report issues. Contributions and improvements are always welcome!  

## License  

This project is released under the MIT License.  

---
