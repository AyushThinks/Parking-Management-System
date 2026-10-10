# Backup and Recovery Notes

The database is stored locally at `data/parking.db` and is excluded from Git.

## Manual backup
1. Close the application to avoid copying a database during active writes.
2. Copy `data/parking.db` to a dated backup location.
3. Keep backups outside the project folder and do not commit customer/vehicle records to GitHub.

## Recovery
1. Close the application.
2. Preserve a copy of the current database for investigation.
3. Replace `data/parking.db` with a known-good backup.
4. Start the application and verify record counts and recent entries.

This is a manual procedure, not an automated backup feature. Test it with sample data before relying on it.
