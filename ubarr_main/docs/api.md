*** Post/ "register"
 - creates a user after recieving an OTP(one-time-password)
- request body :
```json
  {
    "phone_number": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "password": "string"    
  }

**Response **

```json
{
     "phone_number": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "password": "string"    
  }


______________________________________-
*** Post/ "login"
 - login endpoint for the registered users
- request body :
```json
  {
    "phone_number": "string",
  "password": "string"    
  }

**Response **

-if login succesful:
```json

{
     "message": "Login successful"        
  }

-if login fails:
```json

{
     "ValidationError": "Invalid credentials"        
  }

-if login fails 3 times:
```json

{
     "error": "User is blocked for 1 hour"       
  }

___________________________________
*** Post/ "otp/send"
 - gets the phone number from the user and sends the otp to the given number
- request body :
```json
  {
    "phone_number": "string",
  }

**Response **

```json
{
    "message": "OTP sent successfully"   
  }


_________________________________
*** Post/ "otp/verify"
 - gets the otp from the user and does the verification
- request body :
```json
  {
    "otp": "string",
  }

**Response **

-if the otp matches the code:
```json
{
    "message": "OTP verified successfully"   
  }

-if the otp  doesn't match the code:
```json
{
    "error": "Invalid or expired OTP"   
  }



