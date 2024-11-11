FROM node:20-alpine as build

WORKDIR /app

# Cache package installation
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm install -g npm@latest && npm install

COPY . .

# If necessary, you can run npm update here, but ideally not on every build
# RUN npm update

# (Opcional) Verifique dependências obsoletas (para depuração)
# RUN npm outdated

#RUN npm audit fix --force

# Defina a variável de ambiente para a configuração (descomente se necessário)
ENV ENV_FILE_PATH=/app/.env

# Construa a aplicação para produção
RUN npm run build

# Exponha a porta na qual o servidor estará rodando
EXPOSE 3001

# Comando para rodar o frontend
CMD ["npm", "start"]


