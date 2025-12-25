# Database Implementation Guide for Usage Statistics

## Current Implementation (JSON File)

**Location**: `backend/usage_stats.json`

**How it works:**
- Data is stored in a simple JSON file on the server
- Data **persists** when you stop and restart the server
- Data is **lost** if the file is deleted or the server is wiped

**Important Notes:**
- The file survives server restarts (stopping/starting is fine)
- The file does NOT survive if you redeploy to a new server without copying it
- Always download CSV backups before major changes

## When to Switch to a Database

Switch to a database when:
- You're deploying to production/WordPress
- You need to handle 100+ users regularly
- You want automatic backups
- You have multiple server instances
- Data loss is unacceptable

## Database Options for Webmaster

### Option 1: PostgreSQL (Recommended)
**Best for**: Most production deployments

**Free Hosting Options:**
- Supabase (free tier: 500MB)
- Neon (free tier: 3GB)
- ElephantSQL (free tier: 20MB)
- Railway (free trial)

**Setup Time:** 15 minutes
**Code Changes:** Minimal (~50 lines)

### Option 2: MySQL
**Best for**: If your WordPress host already has MySQL

**Setup:**
- Use the same MySQL database as WordPress
- Create a separate table for chatbot usage
- No additional hosting costs

**Setup Time:** 10 minutes
**Code Changes:** Minimal (~50 lines)

### Option 3: MongoDB
**Best for**: If you prefer NoSQL or have MongoDB experience

**Free Hosting:**
- MongoDB Atlas (free tier: 512MB)

**Setup Time:** 20 minutes
**Code Changes:** Minimal (~40 lines)

### Option 4: SQLite
**Best for**: Low traffic, simple deployment

**Pros:**
- No separate database server needed
- File-based like JSON but more reliable
- Better than JSON, not as robust as PostgreSQL

**Setup Time:** 5 minutes
**Code Changes:** Minimal (~30 lines)

## Implementation Instructions

### Step 1: Choose Your Database

Based on your needs, pick from the options above.

### Step 2: Get Database Credentials

You'll need:
- Database URL/connection string
- Username and password
- Database name

### Step 3: Update the Code

I've prepared the code structure to make switching easy. You'll need to:

1. Install database library:
   ```bash
   pip install psycopg2-binary  # For PostgreSQL
   # OR
   pip install pymysql          # For MySQL
   # OR
   pip install pymongo          # For MongoDB
   ```

2. Update `backend/app/services/usage_tracker.py` to use database instead of JSON
3. Add database URL to environment variables
4. Run database migration to create tables

### Step 4: Database Schema

The usage data table will have these columns:

```sql
CREATE TABLE chatbot_usage (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    session_start TIMESTAMP NOT NULL,
    session_end TIMESTAMP,
    age INTEGER,
    location VARCHAR(255),
    gender VARCHAR(50),
    cancer_type VARCHAR(255),
    cancer_stage VARCHAR(255),
    comorbidities TEXT[],
    prior_treatments TEXT[],
    messages_sent INTEGER DEFAULT 0,
    trials_found INTEGER DEFAULT 0,
    total_duration_seconds FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 5: Environment Variables

Add to your `.env` file:

```bash
# For PostgreSQL
DATABASE_URL=postgresql://username:password@host:port/database_name

# For MySQL
DATABASE_URL=mysql://username:password@host:port/database_name

# For MongoDB
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name
```

## Migration Path (From JSON to Database)

When you're ready to switch:

1. **Export existing data**: Use the CSV export from admin dashboard
2. **Set up new database**: Follow steps above
3. **Deploy updated code**: With database connection
4. **Import old data** (optional): Use CSV import tool
5. **Delete JSON file**: Once you confirm database is working

## Code Changes Required

### File: `backend/app/services/usage_tracker.py`

Replace the JSON file operations with database queries. The function signatures stay the same:
- `track_session_start()` → INSERT new record
- `track_intake_form()` → UPDATE record
- `track_message()` → UPDATE record
- `track_trials_found()` → UPDATE record
- `track_session_end()` → UPDATE record
- `get_all_usage_data()` → SELECT all records
- `clear_usage_data()` → DELETE all records (or TRUNCATE table)

### File: `backend/app/main.py`

Add database connection on startup:

```python
from app.database import init_db

@app.on_event("startup")
async def startup_event():
    """Initialize database connection"""
    await init_db()
    # ... rest of startup code
```

## Estimated Implementation Time

- **PostgreSQL/MySQL**: 30-45 minutes
- **MongoDB**: 45-60 minutes
- **SQLite**: 15-20 minutes

## Cost Comparison

| Option | Free Tier | Paid Plans Start At |
|--------|-----------|---------------------|
| PostgreSQL (Supabase) | ✅ 500MB | $25/month |
| PostgreSQL (Neon) | ✅ 3GB | $19/month |
| MySQL (Shared Host) | Often included | $5/month |
| MongoDB Atlas | ✅ 512MB | $9/month |
| SQLite | ✅ Free forever | N/A (file-based) |

## Backup Strategy

### Current (JSON File)
- Manual: Download CSV from admin dashboard weekly
- Automatic: Add cron job to copy `usage_stats.json` daily

### Database
- Most hosted databases include automatic daily backups
- Set up weekly CSV exports as secondary backup
- Enable point-in-time recovery (available on paid plans)

## Security Considerations

### Current (JSON File)
- File is only accessible by the server
- No network exposure
- Risk: If someone gets server access, they can read the file

### Database
- Use environment variables for credentials (never commit to git)
- Use SSL/TLS for database connections
- Enable IP whitelisting if available
- Use read-only credentials for analytics

## Performance Comparison

| Metric | JSON File | SQLite | PostgreSQL | MySQL | MongoDB |
|--------|-----------|--------|------------|-------|---------|
| Reads (100 records) | ~5ms | ~2ms | ~10ms | ~10ms | ~8ms |
| Writes | ~10ms | ~5ms | ~15ms | ~15ms | ~12ms |
| Max Records | ~10K | ~100K | Millions | Millions | Millions |
| Concurrent Users | 1-10 | 10-50 | 1000+ | 1000+ | 1000+ |

## Questions for Your Webmaster

Before implementing database:

1. **Do you already have a database?** (e.g., WordPress MySQL)
   - If yes, we can use that for free

2. **What's your expected traffic?**
   - <100 users/day: JSON or SQLite is fine
   - 100-1000 users/day: PostgreSQL or MySQL
   - 1000+ users/day: PostgreSQL with paid hosting

3. **Do you want to manage the database yourself or use a hosted service?**
   - Hosted = easier, may cost money
   - Self-hosted = more control, requires expertise

4. **What's your backup preference?**
   - Manual CSV downloads
   - Automatic daily backups
   - Both

## Testing Before Production

To test database implementation without affecting production:

1. Set up a test database (free tier)
2. Deploy to a staging environment
3. Generate test data
4. Verify admin dashboard still works
5. Test CSV export
6. Once confirmed, deploy to production

## Need Help?

When ready to implement database:
1. Choose your database option
2. Get credentials from your hosting provider
3. Share your choice and I can provide the exact code changes needed
4. Estimated implementation: 1-2 hours total

## Current File Location

The JSON file is stored at:
```
backend/usage_stats.json
```

To backup manually:
1. Download CSV from admin dashboard, OR
2. Copy the `usage_stats.json` file directly from the server
