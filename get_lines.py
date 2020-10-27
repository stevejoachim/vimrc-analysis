def remove_inline_comment(s):
    i = len(s) - 1
    while i >= 0:
        if s[i] == '"':
            return s[:i]
        i -= 1
    return s


def format_leader(line):
    line = line.replace('"', "'")
    if "','" in line:
        return "Comma"
    elif "' '" in line or "'\<Space>'" in line:
        return "Space"
    elif "';'" in line:
        return "Semicolon"
    elif "'\\'" in line:
        return "Slash"
    else:
        return line


def format_map(line):

    map_syns = {
        "<c": "<C",
        "<down>": "<DOWN>",
        "<Down>": "<DOWN>",
        "<up>": "<UP>",
        "<Up>": "<UP>",
        "<Right>": "<RIGHT>",
        "<right>": "<RIGHT>",
        "<Left>": "<LEFT>",
        "<left>": "<LEFT>",
        "<esc>": "<ESC>",
        "<Esc>": "<ESC>",
        "<leader>": "<Leader>",
        "<cr>": "<CR>",
        "<End>": "<END>",
        "<end>": "<END>",
        "<Space>": "<SPACE>",
        "<space>": "<SPACE>",
        "<m": "<M",
    }

    map_args = ["<silent>"]

    for k, v in map_syns.items():
        line = line.replace(k, v)

    words = line.split()[1:]

    if not words:
        return line

    if words[0] in map_args:
        words = words[1:]

    lhs = words[0]
    rhs = "".join(words[1:])

    return lhs + " → " + rhs


def format_plugin(line):
    if line.count("'") >= 2:
        start = line.index("'")
        end = line.index("'", start + 1)
        line = line[start + 1 : end]
    return remove_inline_comment(line).strip()


def format_setting(line):
    return remove_inline_comment(line).strip()


def get_lines(vimrcs):

    keywords = [
        "endif",
        "endfunction",
        "else",
        "endfor",
        "return",
        "endfun",
        "\\",
        "'",
        '"',
        "au",
        "end",
        "try",
        "call",
    ]

    plug_keywords = [
        "Plug",
        "Plugin",
        "Bundle",
        "NeoBundle",
        "MyNeoBundle",
        "MyNeoBundleLazy",
        "MyNeoBundleNeverLazy",
        "MyNeoBundleNoLazyForDefault",
    ]

    settings, maps, plugins, leaders = [], [], [], []
    for key, value in vimrcs.items():

        # Break vimrc into lines
        lines = value["content"].decode("UTF-8").split("\n")

        for line in lines:

            # Filter out comment and keyword lines, sort into categories
            line = line.strip()
            if line and not any(line.startswith(keyword) for keyword in keywords):

                if "mapleader" in line:
                    leaders.append(format_leader(line))

                elif "map" in line:
                    maps.append(format_map(line.strip()))

                elif any(line.startswith(word) for word in plug_keywords):
                    plugins.append(format_plugin(line.strip()))

                else:
                    settings.append(format_setting(line))

    return settings, maps, plugins, leaders
