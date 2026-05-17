import os

from cumulusci.core.dependencies.dependencies import PackageNamespaceVersionDependency
from cumulusci.core.exceptions import TaskOptionsError
from cumulusci.tasks.salesforce import BaseSalesforceApiTask


class EnsureLitifyInstalled(BaseSalesforceApiTask):
    task_options = {
        "namespace": {
            "description": "The Litify package namespace.",
            "required": False,
        },
        "version": {
            "description": "Fallback Litify version to install when the target org has no Litify package.",
            "required": False,
        },
        "version_env_name": {
            "description": "Environment variable that can override the fallback Litify version.",
            "required": False,
        },
    }

    def _run_task(self):
        namespace = self.options.get("namespace") or "litify_pm"
        installed_versions = self.org_config.installed_packages.get(namespace)

        if installed_versions:
            versions = ", ".join(str(version.number) for version in installed_versions)
            self.logger.info(
                f"Litify namespace {namespace} is already installed ({versions}); skipping install."
            )
            return

        env_name = self.options.get("version_env_name") or "LITIFY_VERSION"
        version = os.environ.get(env_name) or self.options.get("version")

        if not version:
            raise TaskOptionsError(
                f"Litify is not installed in this org. Set {env_name} or provide a fallback version."
            )

        self.logger.info(
            f"Litify namespace {namespace} is not installed; installing bootstrap version {version}."
        )
        PackageNamespaceVersionDependency(
            namespace=namespace,
            version=str(version),
            package_name="Litify",
        ).install(self.project_config, self.org_config)
        self.org_config.reset_installed_packages()
