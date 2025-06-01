[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 💎 Etimo Diamonds 2

Diamonds is a programming challenge. Program a bot and compete to get the highest score. For more information:

- [Project Specification](https://docs.google.com/document/d/13cbmMVXviyu8eKQ6heqgDzt4JNNMeAZO/edit)
- [Get Started with Diamonds](https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit)

## How to build 🔨

1. Clone this repository and move to the root of this project's directory

   ```
   git clone https://github.com/haziqam/tubes1-IF2110-game-engine.git
   cd ./tubes1-IF2110-game-engine
   ```

2. Install dependencies

   ```
   yarn
   ```

3. Setup default environment variables

   For windows

   ```
   ./scripts/copy-env.bat
   ```

   For Linux /(possibly) macOS

   ```
   chmod +x ./scripts/copy-env.sh
   ./scripts/copy-env.sh
   ```

4. Setup local database

   ```
   docker compose up -d database
   ```

   For windows

   ```
   ./scripts/setup-db-prisma.bat
   ```

   For Linux /(possibly) macOS

   ```
   chmod +x ./scripts/setup-db-prisma.sh
   ./scripts/setup-db-prisma.sh
   ```

5. Build

   ```
   npm run build
   ```

## How to Run 💻

```
npm run start
```

Frontend: http://localhost:8082

Swagger (API docs): http://localhost:3000/docs

## Credits 🪙

This repository is adapted from https://github.com/Etimo/diamonds2

Some code in this repository is adjusted to fix some issues in the original repository and to adapt to the requirements of Algorithm Strategies course (IF2211), Informatics Undergraduate Program, ITB.

©️ All rights and credits reserved to [Etimo](https://github.com/Etimo)
