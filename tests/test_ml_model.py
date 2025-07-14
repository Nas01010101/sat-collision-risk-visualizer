import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import importlib
import types

class FakeArray:
    def __init__(self, data):
        self.data = data
    @property
    def shape(self):
        if not self.data:
            return (0, 0)
        first = self.data[0]
        return (len(self.data), len(first) if isinstance(first, list) else 1)
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return FakeArray(self.data[idx])
        elif isinstance(idx, tuple):
            rows, cols = idx
            row_data = self.data[rows] if not isinstance(rows, slice) else self.data[rows]
            if not isinstance(rows, slice):
                row_data = [row_data]
            if isinstance(cols, slice):
                result = [r[cols] for r in row_data]
            else:
                result = [r[cols] for r in row_data]
                return FakeArray(result)
            return FakeArray(result)
        else:
            return self.data[idx]
    def tolist(self):
        return self.data

class DummyDF:
    def __getitem__(self, item):
        return self
    def to_numpy(self, dtype=float):
        return FakeArray([[0,0,0,0,0] for _ in range(10)])

class DummyModel:
    def predict_proba(self, X):
        return FakeArray([[0.0, 1.0] for _ in range(len(X))])

def test_predict_risks_monkeypatched():
    pd_stub = types.ModuleType('pandas')
    pd_stub.read_parquet = lambda path: DummyDF()
    joblib_stub = types.ModuleType('joblib')
    joblib_stub.load = lambda path: DummyModel()
    sys.modules['pandas'] = pd_stub
    sys.modules['joblib'] = joblib_stub

    ml_model = importlib.import_module('backend.ml_model')
    result = ml_model.predict_risks([{'line1': 'foo', 'line2': 'bar'}])
    assert result == [1.0]
