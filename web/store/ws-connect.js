function wsWatcher (store) {
  function msg_receiver (msg) {
    store.messages.push(msg);
  }

  store.$subscribe((mutation, state) => {
    if (mutation.events.key == 'selected_room') {
      if (store.selected_room !== null) {
        store.current_org.wrapper.connect_to_room(
          store.current_org.id,
          store.current_room.id,
          msg_receiver
        );
      }
    }
  });
}

export default wsWatcher;
