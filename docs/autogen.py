import importlib
import inspect

PAGE = [
    {
        'page': 'executable.md',
        'module': 'modules.executable'
    },
    {
        'page': 'load_dataset/load_data.md',
        'module': 'modules.load_dataset.load_data'
    }
]


def process_doc(doc, name):
    if not doc:
        return ''
    lines = doc.split('\n')
    lines = map(lambda x: x.strip(), lines)
    ret = ['##' + name]
    last_tag = ''
    for line in lines:
        if line.endswith(':'):
            last_tag = line
            line = '**' + line + '**\n'
        elif last_tag and line:
            line = '* ' + line + '\n'
        ret.append(line)
    return '\n'.join(ret) + '\n'


if __name__ == '__main__':
    for page in PAGE:
        with open(page['page'], 'w') as output_file:
            module_name = page['module']
            current_module = importlib.import_module(module_name)
            output_file.write('#' + module_name + '\n')
            for _, obj in inspect.getmembers(current_module):
                if inspect.isclass(obj) or inspect.isfunction(obj):
                    if obj.__module__ != module_name:
                        continue
                    output_file.write(process_doc(obj.__doc__, obj.__name__))
                    for method in inspect.getmembers(obj, predicate=inspect.isfunction):
                        output_file.write(process_doc(method[1].__doc__, obj.__name__ + '.' + method[1].__name__))
            output_file.close()
            # search_path('../modules')
