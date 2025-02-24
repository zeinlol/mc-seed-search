# Import the module

# Allow Java modules to be imported
import jpype.imports

# Import all standard Java types into the global scope

# Import each of the decorators into the global scope

# Start JVM with Java types on return
jpype.startJVM(convertStrings=False)

# Import default Java packages
# import java.lang
import java.util

gen = java.util.Random()
print(gen.nextInt(10))
