from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db.utils import OperationalError
import sys

class Command(BaseCommand):
    """
    Health check command that verifies:
    1. Database connection
    2. Database migrations have been applied
    3. Django is ready for dependant services
    """

    def handle(self, *args, **options):
        try:    
            self.stdout.write("Running health check...")
            # Check 1: Database connection
            # Check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            # Check 2: All migrations have been applied
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())

            if plan:
                # There are pending migrations
                self.stderr.write(f"Pending migrations: {len(plan)}")
                sys.exit(1)
        

            self.stdout.write("All health checks passed")

        except OperationalError:
            self.stderr.write("Database connection failed")
            sys.exit(1)
        
        except Exception as e:
            self.stderr.write(f"Health check failed: {e}")
            sys.exit(1)