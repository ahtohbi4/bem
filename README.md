Плагин для Sublime Text 2 и БЭМ [![Codacy Badge](https://api.codacy.com/project/badge/grade/ee9bd49152dd404194dd25debc7a7415)](https://www.codacy.com/app/alexandr-post/sublime-text-bem-creator)
===============================

Плагин позволяет одной командой, не выходя из редактора, создавать БЭМ-сущности и заготовки файлов-технологий

* *.bemhtml
* *.css
* *.deps.js
* *.js

Использование
-------------

С помощью плагина можно создавать такие сущности, как блок, модификатор блока, элемент и модификатор элемента. Ctrl+Alt+b или "Popup menu" > "BEM" > "Create" для вызова строки ввода комманды.

**Создание блока:**

Команда
```
    blockName
```

Создаст
```
    path_to_blocks_dir/
        blocks/
            blockName/
                blockName.bemhtml
                blockName.css
                blockName.deps.js
                blockName.js
```

**Создание модификатора блока:**

Команда
```
    blockName_modName_modValue
```

Создаст
```
    path_to_blocks_dir/
        blocks/
            blockName/
                blockName.deps.js (создается, если до этого блока blockName не существовало)
                _modName/
                    blockName_modName_modValue.bemhtml
                    blockName_modName_modValue.css
                    blockName_modName_modValue.js
```

**Создание элемента:**

Команда
```
    blockName__elemName
```

Создаст
```
    path_to_blocks_dir/
        blocks/
            blockName/
                blockName.deps.js (создается, если до этого блока blockName не существовало)
                __elemName/
                    blockName__elemName.bemhtml
                    blockName__elemName.css
                    blockName__elemName.js
```

**Создание модификатора элемента:**

Команда
```
    blockName__elemName_modName_modValue
```

Создаст
```
    path_to_blocks_dir/
        blocks/
            blockName/
                blockName.deps.js (создается, если до этого блока blockName не существовало)
                __elemName/
                    _modName/
                        blockName__elemName_modName_modValue.bemhtml
                        blockName__elemName_modName_modValue.css
                        blockName__elemName_modName_modValue.js
```
