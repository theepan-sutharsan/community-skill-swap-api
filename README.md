1. Create VENV
    python -m venv .venv

2. Activate Venv
    .venv\Scripts\activate

3. pip install -r requirements.txt

4. Create .env file
    DB_USER=root
    DB_PASSWORD=yourpassword
    DB_HOST=localhost
    DB_NAME=skillswap
    JWT_SECRET_KEY=your-secret-key
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES=60
    FLASK_DEBUG=1
5. py run.py

POST /api/auth/login
POST /api/auth/register

API Endpoints

/api/auth

POST    /register
POST    /login    
GET     /me     

/api/users

 GET     /              admin           List all users   
 GET     /:user_id      admin, member   Get user         
 PUT     /:user_id      admin, member   Update user      
 DELETE  /:user_id      admin           Delete user      

/api/skills

 GET     /              No   
 GET     /:skill_id     No   
 POST    /              admin
 PUT     /:skill_id     admin
 DELETE  /:skill_id     admin
 POST    /import-csv    admin
 GET     /export/csv    admin
 GET     /export/pdf    admin

/api/user-skills

 GET     /              member, admin
 POST    /              member       
 GET     /:entry_id     member, admin
 PUT     /:entry_id     member       
 DELETE  /:entry_id     member       

/api/swap

 GET      /                   member, admin
 POST     /                   member       
 GET      /:swap_id           member, admin
 PUT      /:swap_id/respond   member       
 DELETE   /:swap_id           member       


/api/sessions

 GET     /                 member, admin 
 POST    /                 member        
 GET     /:session_id      member, admin 
 PUT     /:session_id      member        
 DELETE  /:session_id      member        

/api/dashboard

 GET     /        member, admin

