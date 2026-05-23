from contextlib import contextmanager

CHECK_MARK = "✓"  # Unicode check (✔ / ✓)
X_MARK = "✗"  # Unicode cross (✘ / ✗)


@contextmanager
def log_action(description: str):
    """
    Gestor de contexto (Context Manager) para registrar el resultado de una acción.

    Si el bloque dentro del `with` finaliza exitosamente, imprime: [✓] mensaje
    Si ocurre algún error (como un NoSuchElementException o TimeoutException),
    imprime: [✗] mensaje y relanza la excepción.
    """
    try:
        yield
        print(f"[{CHECK_MARK}] {description}")
    except Exception as e:
        print(f"[{X_MARK}] {description}")
        raise e
