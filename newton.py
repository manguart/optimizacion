import math
f = lambda x: math.exp(-x) - x
df = lambda x: -math.exp(-x) - 1

def newton(f, df, x0, epsilon):
    x_i = x0
    fx_i = f(x0)
    while abs(fx_i) > epsilon:
        dfx_i = df(x_i)
        x_i = x_i - fx_i/dfx_i
        fx_i = f(x_i)
    return x_i

newton(f, df, 1, 1e-8)



%spark.pyspark
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit

df_assembler = VectorAssembler(inputCols=['longitud', 'latitud'], outputCol='features')
profeco = df_assembler.transform(df)
model_profeco = titanic.select(['features','precio'])
train_df,test_df = model_profeco.randomSplit([0.8,0.2])

rf=RandomForestRegressor(labelCol='precio')
paramGrid = ParamGridBuilder()\
    .addGrid(rf.maxDepth, [5, 10, 20]) \
    .addGrid(rf.numTrees, [20, 50, 75]) \
    .build()

tvs = TrainValidationSplit(estimator=rf, estimatorParamMaps=paramGrid,evaluator=RegressionEvaluator(labelCol='precio'),trainRatio=0.8)
model2 = tvs.fit(train_df)
model2_predictions= model2.transform(test_df)