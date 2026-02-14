import re
from typing import List, Dict, Set

class NetlistParser:
    """Parses Protel Netlist 2.0 format (tagged format)."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.components: Dict[str, Dict] = {}
        self.nets: Dict[str, List[str]] = {}
        self.parse()

    def parse(self):
        """Iterates through tagged blocks in the .NET file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
                content = f.read()
                
            # 1. Parse Component Blocks [ ]
            comp_blocks = re.findall(r'\[(.*?)\]', content, re.DOTALL)
            for block in comp_blocks:
                lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
                if lines and lines[0] == 'DESIGNATOR':
                    self._parse_component_block(lines)
            
            # 2. Parse Net Blocks ( ) - Common in Telesis/Protel
            net_blocks = re.findall(r'\((.*?)\)', content, re.DOTALL)
            for block in net_blocks:
                lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
                if lines:
                    net_name = lines[0]
                    self.nets[net_name] = lines[1:]

            # 3. Fallback for [NETNAME] style blocks
            for block in comp_blocks:
                lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
                if lines and lines[0] == 'NETNAME':
                    self._parse_net_block(lines)
                    
        except Exception as e:
            print(f"Error parsing netlist: {e}")

    def _parse_component_block(self, lines: List[str]):
        data = {}
        i = 0
        while i < len(lines):
            tag = lines[i]
            if i + 1 < len(lines):
                # Check if next line is a tag (starts with uppercase or is a known tag)
                # But in Protel 2.0, tags are followed by values on the next line.
                # However, some values might be empty or multi-line (rare in this format).
                # Simplified: every odd line is a tag, every even line is a value.
                # Actually, the format is [TAG\nVALUE\nTAG\nVALUE]
                val = lines[i+1]
                data[tag] = val
                i += 2
            else:
                i += 1
        
        designator = data.get('DESIGNATOR')
        if designator:
            self.components[designator] = data

    def _parse_net_block(self, lines: List[str]):
        net_name = None
        pins = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line == 'NETNAME':
                if i + 1 < len(lines):
                    net_name = lines[i+1]
                i += 2
            elif line == 'PIN':
                if i + 1 < len(lines):
                    pins.append(lines[i+1])
                i += 2
            else:
                i += 1
        
        if net_name:
            self.nets[net_name] = pins

    def get_net_names(self) -> List[str]:
        return list(self.nets.keys())

    def get_net_pins(self, net_name: str) -> List[str]:
        return self.nets.get(net_name, [])

    def get_component_nets(self, designator: str) -> Dict[str, str]:
        """Returns a mapping of pin -> net_name for a given component."""
        mapping = {}
        for net_name, pins in self.nets.items():
            for pin_entry in pins:
                # Pin entry is typically "U1-A5"
                if '-' in pin_entry:
                    comp, pin = pin_entry.split('-', 1)
                    if comp == designator:
                        mapping[pin] = net_name
        return mapping
