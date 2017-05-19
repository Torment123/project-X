import importlib

"""This module is responsible for the generation of executables from solutions"""


class Pipeline:
    """Execute the provided solution in form of configs.

    Pipeline is a class take configs as inputs and execute them.

    Attributes:
        configs: An array of MethodConfig.
        calls: An array of MethodCalls.
    """
    def __init__(self, configs):
        self.configs = configs
        self.calls = []

    def run(self):
        """Run the pipeline of functions.
        
        Returns:
            The return value of the last function call.
        """
        for config in self.configs:
            call = self.generate_call(config)
            call.execute()
            self.calls.append(call)
        return self.calls[-1].output

    def generate_call(self, config):
        """Generates a MethodCall instance.

        From a MethodConfig, it generates the required MethodCall by replacing the
        references in parameters.

        Args:
            config: An instance of MethodConfig to be converted to MethodCall.
    
        Returns:
            A MethodCall instance with real values in the params.
    
        Raises:
            ValueError: An error occurred when the category of the replacement is not recognized.
        """
        for i, replace in enumerate(config.replacement_list):
            if not replace:
                continue
            replacement_info = config.params[i]
            if replacement_info.category == 'target':
                config.params[i] = self.calls[replacement_info.call_index].target
            elif replacement_info.category == 'input':
                config.params[i] = self.calls[replacement_info.call_index].params[replacement_info.sub_index]
            elif replacement_info.category == 'output':
                if replacement_info.sub_index:
                    config.params[i] = self.calls[replacement_info.call_index].output[replacement_info.sub_index]
                else:
                    config.params[i] = self.calls[replacement_info.call_index].output
            else:
                raise ValueError('Category %s not recognized.' % replacement_info.category)
        return MethodCall(config.target, config.method, config.params, config.need_import)


class Replacement:
    def __init__(self, category, call_index, sub_index=None):
        if category not in ['target', 'input', 'output']:
            raise ValueError('Category %s not recognized.' % category)

        self.sub_index = sub_index
        self.call_index = call_index
        self.category = category


class MethodConfig:
    def __init__(self, target, method, need_import, params, replacement_list=None):
        if not replacement_list:
            self.replacement_list = [None] * len(params)
        else:
            self.replacement_list = replacement_list
        self.method = method
        self.params = params
        self.need_import = need_import
        self.target = target


class MethodCall:
    def __init__(self, target, method, params, need_import=True):
        self.module = target
        if need_import:
            self.module = importlib.import_module(target)
        self.method = getattr(self.module, method)
        self.params = params
        self.output = None

    def execute(self):
        self.output = self.method(*self.params)
        return self.method(*self.params)
