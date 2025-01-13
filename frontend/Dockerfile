FROM node:20-alpine AS build

WORKDIR /chat_ui_with_ollama

COPY package.json .

RUN npm install

COPY . .

RUN npm run build

FROM node:20-alpine AS production

WORKDIR /chat_ui_with_ollama

COPY package.json .
RUN npm install

COPY --from=build /chat_ui_with_ollama/dist/ /chat_ui_with_ollama/dist/

EXPOSE 7066

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "7066"]