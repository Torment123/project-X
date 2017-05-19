#modules.executable
##Pipeline
Execute the provided solution in form of configs.

Pipeline is a class take configs as inputs and execute them.

**Attributes:**

* configs: An array of MethodConfig.

* calls: An array of MethodCalls.


##Pipeline.generate_call
Generates a MethodCall instance.

From a MethodConfig, it generates the required MethodCall by replacing the
references in parameters.

**Args:**

* config: An instance of MethodConfig to be converted to MethodCall.


**Returns:**

* A MethodCall instance with real values in the params.


**Raises:**

* ValueError: An error occurred when the category of the replacement is not recognized.


##Pipeline.run
Run the pipeline of functions.

**Returns:**

* The return value of the last function call.


