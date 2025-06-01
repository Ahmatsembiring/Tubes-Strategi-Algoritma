@echo off
echo Navigating to directory: packages/backend
cd packages/backend || exit /b 1

echo Install dependencies
call yarn install

echo Update the database schema
call npx prisma db push

echo Seed the database
call npx prisma db seed
