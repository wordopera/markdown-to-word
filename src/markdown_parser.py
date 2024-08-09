import re

class MarkdownParser:
    def __init__(self):
        self.patterns = {
            'header': r'^(#{1,6})\s(.+)$',
            'unordered_list': r'^\s*[-*+]\s(.+)$',
            'ordered_list': r'^\s*(\d+)\.\s(.+)$',
            'task': r'^\s*- \[([ x])\]\s(.+)$',
        }

    def parse(self, markdown_text):
        lines = markdown_text.split('\n')
        elements = []
        in_code_block = False
        code_block_content = []

        for line in lines:
            if line.strip().startswith('```'):
                if in_code_block:
                    elements.append(('code_block', '\n'.join(code_block_content)))
                    code_block_content = []
                in_code_block = not in_code_block
                continue

            if in_code_block:
                code_block_content.append(line)
                continue

            element = self.parse_line(line)
            if element:
                elements.append(element)

        return elements

    def parse_line(self, line):
        for element_type, pattern in self.patterns.items():
            match = re.match(pattern, line)
            if match:
                if element_type == 'header':
                    return (f'h{len(match.group(1))}', match.group(2))
                elif element_type == 'ordered_list':
                    return ('ordered_list', match.group(2), int(match.group(1)))
                elif element_type == 'task':
                    return ('task', match.group(2), match.group(1) == 'x')
                else:
                    return (element_type, match.group(1))

        return ('paragraph', line) if line.strip() else None