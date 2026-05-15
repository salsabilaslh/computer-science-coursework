from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# load dataset
wine = load_wine()

# feature selection (3 features)
X = wine.data[:, [0, 1, 2]]

# target
y = wine.target

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# create model
model = RandomForestClassifier()

# train model
model.fit(X_train, y_train)
