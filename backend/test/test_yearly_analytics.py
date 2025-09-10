#!/usr/bin/env python3
"""
Test script for yearly analytics API (B0302)
"""

import asyncio
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories.instagram_repository import instagram_repository
from api.analytics import get_yearly_analytics
from models.user import User

async def test_yearly_analytics():
    """Test yearly analytics API functionality"""
    print("🧪 Testing Yearly Analytics API (B0302)")
    print("=" * 50)
    
    # Test data
    test_account_id = "mock_account_1"  # Assuming this exists
    mock_user = User(id=1, username="test", password_hash="test_hash", created_at="2025-01-01")
    
    try:
        # Test 1: Repository methods
        print("\n📊 Testing Repository Methods:")
        
        print("1. Testing get_monthly_account_stats...")
        account_stats = await instagram_repository.get_monthly_account_stats(test_account_id)
        print(f"   Account stats: {len(account_stats)} months found")
        if account_stats:
            print(f"   Sample: {account_stats[0]}")
        
        print("2. Testing get_monthly_media_aggregation...")
        media_stats = await instagram_repository.get_monthly_media_aggregation(test_account_id)
        print(f"   Media stats: {len(media_stats)} months found")
        if media_stats:
            print(f"   Sample: {media_stats[0]}")
        
        print("3. Testing get_total_posts_count...")
        total_posts = await instagram_repository.get_total_posts_count(test_account_id)
        print(f"   Total posts: {total_posts}")
        
        # Test 2: Full API endpoint
        print("\n🎯 Testing Full API Endpoint:")
        try:
            result = await get_yearly_analytics(test_account_id, None, mock_user)
            print(f"   ✅ API Success!")
            print(f"   Account ID: {result.account_id}")
            print(f"   Total Posts: {result.total_posts}")
            print(f"   Avg Engagement Rate: {result.avg_engagement_rate}%")
            print(f"   Monthly Stats: {len(result.monthly_stats)} months")
            
            if result.monthly_stats:
                print(f"   First month: {result.monthly_stats[0].month}")
                print(f"   - Followers: {result.monthly_stats[0].followers_count}")
                print(f"   - Likes: {result.monthly_stats[0].total_likes}")
        
        except Exception as api_error:
            print(f"   ❌ API Error: {api_error}")
        
        # Test 3: Error cases
        print("\n⚠️  Testing Error Cases:")
        try:
            result = await get_yearly_analytics("nonexistent_account", None, mock_user)
            print("   ❌ Should have thrown 404 error")
        except Exception as e:
            print(f"   ✅ Correctly handled error: {type(e).__name__}")
        
        print("\n🎉 Yearly Analytics API Test Complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_yearly_analytics())