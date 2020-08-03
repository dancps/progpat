# VSCode

% Adding a snippet in VSCode

Open the command palette(Ctrl+Shift+P) and type "Preferences: Configure User Snippets"

% Example of Python snippet
{
    "numpy pattern": {
        "scope": "python",
        "prefix": ["np"],
        "body": ["import numpy as np",
        "a = [1,2,3,4,5,6]",
        "np_a = np.array(a)",
        "print(np_a.shape)"
    }
}