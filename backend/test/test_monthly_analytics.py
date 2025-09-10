#!/usr/bin/env python3
"""
Test script for monthly analytics API (B0303)
"""

import asyncio
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories.instagram_repository import instagram_repository
from api.analytics import get_monthly_analytics
from models.user import User

async def test_monthly_analytics():
    """Test monthly analytics API functionality"""
    print("🧪 Testing Monthly Analytics API (B0303)")
    print("=" * 50)
    
    # Test data
    test_account_id = "mock_account_1"  # Assuming this exists
    test_year = 2025
    test_month = 3
    mock_user = User(id=1, username="test", password_hash="test_hash", created_at="2025-01-01")
    
    try:
        # Test 1: Repository methods
        print("\n📊 Testing Repository Methods:")
        
        print(f"1. Testing get_daily_account_stats for {test_year}-{test_month:02d}...")
        account_stats = await instagram_repository.get_daily_account_stats(test_account_id, test_year, test_month)
        print(f"   Account stats: {len(account_stats)} days found")
        if account_stats:
            print(f"   Sample day 1: {account_stats[0]}")
            print(f"   Sample day 15: {account_stats[14] if len(account_stats) > 14 else 'N/A'}")
        
        print(f"2. Testing get_daily_media_stats_aggregation for {test_year}-{test_month:02d}...")
        media_stats = await instagram_repository.get_daily_media_stats_aggregation(test_account_id, test_year, test_month)
        print(f"   Media stats: {len(media_stats)} days found")
        if media_stats:
            print(f"   Sample day 1: {media_stats[0]}")
        
        # Test 2: Full API endpoint
        print("\n🎯 Testing Full API Endpoint:")
        try:
            result = await get_monthly_analytics(test_account_id, test_year, test_month, mock_user)
            print(f"   ✅ API Success!")
            print(f"   Account ID: {result.account_id}")
            print(f"   Month: {result.month}")
            print(f"   Daily Stats: {len(result.daily_stats)} days")
            
            if result.daily_stats:
                print(f"   First day: {result.daily_stats[0].date}")
                print(f"   - Posts: {result.daily_stats[0].posts_count}")
                print(f"   - New Followers: {result.daily_stats[0].new_followers}")
                print(f"   - Reach: {result.daily_stats[0].reach}")
                print(f"   - Profile Views: {result.daily_stats[0].profile_views}")
                print(f"   - Website Clicks: {result.daily_stats[0].website_clicks}")
                
                print(f"   Last day: {result.daily_stats[-1].date}")
                print(f"   - Posts: {result.daily_stats[-1].posts_count}")
                print(f"   - Reach: {result.daily_stats[-1].reach}")
        
        except Exception as api_error:
            print(f"   ❌ API Error: {api_error}")
        
        # Test 3: Error cases
        print("\n⚠️  Testing Error Cases:")
        
        # Test invalid month
        try:
            result = await get_monthly_analytics(test_account_id, test_year, 13, mock_user)
            print("   ❌ Should have thrown 400 error for invalid month")
        except Exception as e:
            print(f"   ✅ Correctly handled invalid month error: {type(e).__name__}")
        
        # Test nonexistent account
        try:
            result = await get_monthly_analytics("nonexistent_account", test_year, test_month, mock_user)
            print("   ❌ Should have thrown 404 error")
        except Exception as e:
            print(f"   ✅ Correctly handled nonexistent account error: {type(e).__name__}")
        
        print("\n🎉 Monthly Analytics API Test Complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_monthly_analytics())