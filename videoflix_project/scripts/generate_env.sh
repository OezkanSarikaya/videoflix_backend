#!/bin/bash

# Erstelle eine .env-Datei mit den GitHub Secrets
echo "DEBUG=${{ secrets.DEBUG }}" > .env
echo "SECRET_KEY=${{ secrets.SECRET_KEY }}" >> .env
echo "DATABASE_NAME=${{ secrets.DATABASE_NAME }}" >> .env
echo "DATABASE_USER=${{ secrets.DATABASE_USER }}" >> .env
echo "DATABASE_PASSWORD=${{ secrets.DATABASE_PASSWORD }}" >> .env
echo "FFMPEG_PATH=${{ secrets.FFMPEG_PATH }}" >> .env
echo "EMAIL_HOST=${{ secrets.EMAIL_HOST }}" >> .env
echo "EMAIL_PORT=${{ secrets.EMAIL_PORT }}" >> .env
echo "EMAIL_USE_TLS=${{ secrets.EMAIL_USE_TLS }}" >> .env
echo "EMAIL_HOST_USER=${{ secrets.EMAIL_HOST_USER }}" >> .env
echo "EMAIL_HOST_PASSWORD=${{ secrets.EMAIL_HOST_PASSWORD }}" >> .env
echo "DEFAULT_FROM_EMAIL=${{ secrets.DEFAULT_FROM_EMAIL }}" >> .env
echo "DJANGO_SETTINGS_MODULE=${{ secrets.DJANGO_SETTINGS_MODULE }}" >> .env
echo "FRONTEND_URL=${{ secrets.FRONTEND_URL }}" >> .env
echo "IMPORT_VIDEO_SOURCE=${{ secrets.IMPORT_VIDEO_SOURCE }}" >> .env
echo "PROTECTED_MEDIA=${{ secrets.PROTECTED_MEDIA }}" >> .env
