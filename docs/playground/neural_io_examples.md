# Playground Neural I/O — Beispiele

## Skalarer Eingang

```python
from mhrn_playground import Playground

pg = Playground(
    n_neurons=128,
    edge_budget=512,
    stimulus="none",
    neural_io_enabled=True,
    neural_io_input_channels=16,
    neural_io_output_channels=16,
    neural_io_input_codec="population_latency_v1",
    neural_io_output_decoder="population_rate_v1",
    neural_io_input_payload=0.72,
    neural_io_window_ticks=16,
    neural_io_input_role="GATEWAY_AFFERENT",
    neural_io_output_role="GATEWAY_EFFERENT",
)

result = pg.run()
io = result["neural_io"]
```

## Vektor-Eingang

```python
pg = Playground(
    n_neurons=128,
    edge_budget=512,
    neural_io_enabled=True,
    neural_io_input_codec="vector_population_v1",
    neural_io_input_payload=[0.1, 0.9, 0.3, 0.0],
)
```

## Symbolischer Eingang

```python
pg = Playground(
    n_neurons=128,
    edge_budget=512,
    neural_io_enabled=True,
    neural_io_input_channels=16,
    neural_io_input_codec="sparse_symbol_v1",
    neural_io_input_payload="QUERY",
    neural_io_output_channels=16,
    neural_io_output_decoder="sparse_symbol_v1",
)
```

Der Rohpayload erscheint niemals in `result`; nur Hash, Größe, Codec- und
Provenienzmetadaten werden ausgegeben.
