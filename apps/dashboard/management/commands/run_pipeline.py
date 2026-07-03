from django.core.management.base import BaseCommand, CommandError

from dashboard.services.pipeline import run_pipeline


class Command(BaseCommand):
    help = "Execute RL agents inference and update the dashboard."

    def handle(self, *args, **options) -> None:
        try:
            run_pipeline()
        except Exception as exc:
            raise CommandError(f"Pipeline failed: {exc}") from exc

        self.stdout.write(self.style.SUCCESS("Pipeline completed successfully."))
