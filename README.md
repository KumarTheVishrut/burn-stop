##### BURNSTOP

### Stop burning , start saving money for your startup, 

## Get insights on your overall subscriptions , cloud-infrastructure ,api keys, added responsibility management for organization , Devs , product managers and CTO's 


## FOSS - no bs - self-hostable all thanks to docker


#### Tech stack


### Frontend - Next.js because why not? 

### Backend - python because why not ?
### ENDPOINTS


# POST    /auth/login
# POST    /auth/signup

# POST    /organizations/          # Create org
# GET     /organizations/          # List orgs (for user)
# GET     /organizations/{org_id}  # Get org details

# POST    /organizations/{org_id}/users    # Add user to org
# DELETE  /organizations/{org_id}/users/{user_id}

# POST    /organizations/{org_id}/services     # Add service
# GET     /organizations/{org_id}/services     # List services
# PUT     /services/{service_id}               # Update service
# DELETE  /services/{service_id}               # Mark for deletion

# GET     /organizations/{org_id}/reminders   # Upcoming reminders
# POST    /reminders/{reminder_id}/acknowledge # Confirm action



### DB - Redis because I love snappy things



#### Docker hosting guide soon


