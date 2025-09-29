#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from repositories.user_repository import user_repository

async def check_users():
    """Check all users in the database"""
    try:
        # This is a simple check - we'll try to get a user by a known username
        test_usernames = ["admin", "shintaitiku", "test", "user"]
        
        print("🔍 Checking users in database...")
        
        for username in test_usernames:
            user = await user_repository.get_by_username(username)
            if user:
                print(f"✅ Found user: '{username}' (ID: {user.id})")
            else:
                print(f"❌ User not found: '{username}'")
                
        # Try to see if we can query the database at all
        print("\n📊 Database connection test...")
        
    except Exception as e:
        print(f"❌ Error checking users: {e}")

if __name__ == "__main__":
    asyncio.run(check_users())