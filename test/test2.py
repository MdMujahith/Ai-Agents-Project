import pkgutil
import google.adk

package = google.adk
for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
    print(f"Found submodule: {modname} (Package: {ispkg})")
