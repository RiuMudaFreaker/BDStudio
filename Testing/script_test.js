io.on("connection", (socket) => {
    socket.on("joinGame", (gameId) => {
      socket.join(gameId);
      socket.emit("joinedGame", { gameId });
      console.log(`Player ${socket.id} joined game ${gameId}`);
    });
  });
  