# Performance Testing DocumentDB using mongo-perf running on Amazon EKS

The architecture below demonstrates a load testing setup to test Amazon DocumentDB using mongo-perf on Amazon Elastic Kubernetes Service (EKS).
### @TODO: Use Fargate Spot for the mongo-perf pod

## Architecture
![architecture](imgs/mongo-perf-eks.png)

## Create DocumentDB Cluster
Follow instructions [here](https://docs.aws.amazon.com/documentdb/latest/developerguide/db-cluster-create.html) to create a DocumentDB cluster.
## Tool
This test uses a dockerized version of [mongo-perf](https://github.com/mongodb/mongo-perf) which is also rolled into a kubernetes deployment.

## (Optional) If you wish to build the image and push it to ECR
1. [Create a ECR repository](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html)
1. git clone https://github.com/satchpx/documentdb-pov-testing.git
1. cd documentdb-pov-testing/perf-test/docker
1. Follow instructions [here](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html) to authenticate with your repository -> build image -> push to ECR 

## Update manifests to pull image from ECR
Update `mongo-perf-job.yaml` and `mongo-perf-deployment.yaml` to update the `image:` specification pull from ECR. For example:
```yaml
     - name: mongodb-perf-tester
        image: 111122223333.dkr.ecr.us-west-2.amazonaws.com/documentdb-perf-tester:1.0
        command: ["/mongo-perf/run"]
```
## Deploy
To run a load test/ Stress test:
```
kubectl apply -f mongo-perf.yaml
```
*NOTE:* This will create a Kubernetes deployment, and will be long running.


To run a performance test on demand:
```
kubectl apply -f mongo-perf-job.yaml
```

## Usage
The test results should be written to `STDOUT` and can be obtained by:
```
kubectl logs <mongodb-perf-podname>
```

To manually get the raw output: 
```
kubectl cp <mongodb-perf-podname>:/tmp/perf.out /tmp/perf.out
```

To run the analysis and pretty print:
```
python3 analyze.py
```

Sample Output:
```
test_name                                      num_threads    ops_per_sec
-------------------------------------------  -------------  -------------
Insert.SingleIndex.Seq                                   1    1848.4
Insert.SingleIndex.Seq                                   2    3496.68
Insert.SingleIndex.Seq                                   4    6473.84
Insert.SingleIndex.Uncontested.Rnd                       1    1723.06
Insert.SingleIndex.Uncontested.Rnd                       2    3423.56
Insert.SingleIndex.Uncontested.Rnd                       4    5593.34
Insert.SingleIndex.Contested.Rnd                         1    1763.39
Insert.SingleIndex.Contested.Rnd                         2    3489.03
Insert.SingleIndex.Contested.Rnd                         4    6131.48
Insert.MultiIndex.Uncontested.Rnd                        1    1770.82
Insert.MultiIndex.Uncontested.Rnd                        2    3277.66
Insert.MultiIndex.Uncontested.Rnd                        4    6190.8
Insert.MultiIndex.Contested.Rnd                          1    1681.76
Insert.MultiIndex.Contested.Rnd                          2    3432.42
Insert.MultiIndex.Contested.Rnd                          4    5918.16
Insert.MultiKeyIndex.Uncontested.Rnd                     1    1715.43
Insert.MultiKeyIndex.Uncontested.Rnd                     2    3316.53
Insert.MultiKeyIndex.Uncontested.Rnd                     4    5796.74
Insert.MultiKeyIndex.Contested.Rnd                       1    1793.15
Insert.MultiKeyIndex.Contested.Rnd                       2    3273.23
Insert.MultiKeyIndex.Contested.Rnd                       4    5949.72
Insert.BigKeyIndex                                       1     571.33
Insert.BigKeyIndex                                       2    1020.82
Insert.BigKeyIndex                                       4    1637.26
Update.SetWithIndex.Random                               1    1610.05
Update.SetWithIndex.Random                               2    3185.81
Update.SetWithIndex.Random                               4    5523.14
Update.SetWithMultiIndex.Random                          1    1594.15
Update.SetWithMultiIndex.Random                          2    3151.84
Update.SetWithMultiIndex.Random                          4    5212.03
Update.SetWithMultiIndex.String                          1    1307.01
Update.SetWithMultiIndex.String                          2    2367.38
Update.SetWithMultiIndex.String                          4    4280.59
Insert.DocValidation.OneInt.Compare                      1    1876.94
Insert.DocValidation.OneInt.Compare                      2    3449.87
Insert.DocValidation.OneInt.Compare                      4    6782.3
Insert.DocValidation.OneInt                              1    1786.98
Insert.DocValidation.OneInt                              2    3599.39
Insert.DocValidation.OneInt                              4    6455.27
Insert.DocValidation.OneInt.JSONSchema                   1    1861.07
Insert.DocValidation.OneInt.JSONSchema                   2    3543.53
Insert.DocValidation.OneInt.JSONSchema                   4    6084.02
Insert.DocValidation.TenInt.Compare                      1    1855.28
Insert.DocValidation.TenInt.Compare                      2    3460.71
Insert.DocValidation.TenInt.Compare                      4    6349.35
Insert.DocValidation.TenInt                              1    1735.74
Insert.DocValidation.TenInt                              2    3384.04
Insert.DocValidation.TenInt                              4    6237.94
Insert.DocValidation.TwentyInt.Compare                   1    1694.07
Insert.DocValidation.TwentyInt.Compare                   2    3442.49
Insert.DocValidation.TwentyInt.Compare                   4    5797.02
Insert.DocValidation.TwentyInt                           1    1697.16
Insert.DocValidation.TwentyInt                           2    3383.33
Insert.DocValidation.TwentyInt                           4    5727.33
Insert.DocValidation.TwentyInt.JSONSchema                1    1724.92
Insert.DocValidation.TwentyInt.JSONSchema                2    3265.51
Insert.DocValidation.TwentyInt.JSONSchema                4    6021.1
Insert.DocValidation.OneFiftyInt.Compare                 1    1291.49
Insert.DocValidation.OneFiftyInt.Compare                 2    2356.64
Insert.DocValidation.OneFiftyInt.Compare                 4    4069.04
Insert.DocValidation.OneFiftyInt                         1     895.29
Insert.DocValidation.OneFiftyInt                         2    1654.63
Insert.DocValidation.OneFiftyInt                         4    2919.09
Insert.DocValidation.OneFiftyInt.JSONSchema              1     923.13
Insert.DocValidation.OneFiftyInt.JSONSchema              2    1581.25
Insert.DocValidation.OneFiftyInt.JSONSchema              4    2981.54
Insert.DocValidation.Variety.Compare                     1    1732
Insert.DocValidation.Variety.Compare                     2    3318.64
Insert.DocValidation.Variety.Compare                     4    6396.06
Insert.DocValidation.Variety.JSONSchema                  1    1654.6
Insert.DocValidation.Variety.JSONSchema                  2    3284.64
Insert.DocValidation.Variety.JSONSchema                  4    5487.41
Insert.DocValidation.Array.Compare                       1    1626.37
Insert.DocValidation.Array.Compare                       2    3184.82
Insert.DocValidation.Array.Compare                       4    5315.38
Insert.DocValidation.Array.JSONSchema                    1    1499.24
Insert.DocValidation.Array.JSONSchema                    2    2674.08
Insert.DocValidation.Array.JSONSchema                    4    4903.93
Insert.DocValidation.Nested.Compare                      1    1713.96
Insert.DocValidation.Nested.Compare                      2    3416.69
Insert.DocValidation.Nested.Compare                      4    6148.15
Insert.DocValidation.Nested.JSONSchema                   1    1673.3
Insert.DocValidation.Nested.JSONSchema                   2    3226.94
Insert.DocValidation.Nested.JSONSchema                   4    5397.8
Update.DocValidation.OneNum.Compare                      1    1719.77
Update.DocValidation.OneNum.Compare                      2    3229
Update.DocValidation.OneNum.Compare                      4    5917.52
Update.DocValidation.OneNum                              1    1756.45
Update.DocValidation.OneNum                              2    3212.33
Update.DocValidation.OneNum                              4    6070.88
Update.DocValidation.OneNum.JSONSchema                   1    1684.09
Update.DocValidation.OneNum.JSONSchema                   2    3343.09
Update.DocValidation.OneNum.JSONSchema                   4    5648.15
Update.DocValidation.TenNum.Compare                      1    1593.44
Update.DocValidation.TenNum.Compare                      2    3077.89
Update.DocValidation.TenNum.Compare                      4    5209.93
Update.DocValidation.TenNum                              1    1677.71
Update.DocValidation.TenNum                              2    3128.83
Update.DocValidation.TenNum                              4    5549.91
Update.DocValidation.TwentyNum.Compare                   1    1549.26
Update.DocValidation.TwentyNum.Compare                   2    2995.2
Update.DocValidation.TwentyNum.Compare                   4    5408.68
Update.DocValidation.TwentyNum                           1    1514.15
Update.DocValidation.TwentyNum                           2    3031.55
Update.DocValidation.TwentyNum                           4    5108.63
Update.DocValidation.TwentyNum.JSONSchema                1    1561.3
Update.DocValidation.TwentyNum.JSONSchema                2    2995.22
Update.DocValidation.TwentyNum.JSONSchema                4    5118.87
Update.DocValidation.OneFiftyNum.Compare                 1     885.796
Update.DocValidation.OneFiftyNum.Compare                 2    1556
Update.DocValidation.OneFiftyNum.Compare                 4    2982.2
Update.DocValidation.OneFiftyNum                         1     695.348
Update.DocValidation.OneFiftyNum                         2    1319.32
Update.DocValidation.OneFiftyNum                         4    2380.06
Update.DocValidation.OneFiftyNum.JSONSchema              1     707.92
Update.DocValidation.OneFiftyNum.JSONSchema              2    1303.33
Update.DocValidation.OneFiftyNum.JSONSchema              4    2334.32
Update.DocValidation.Variety.Compare                     1    1739.12
Update.DocValidation.Variety.Compare                     2    3210.23
Update.DocValidation.Variety.Compare                     4    5941.95
Update.DocValidation.Variety.JSONSchema                  1    1669.78
Update.DocValidation.Variety.JSONSchema                  2    3003.63
Update.DocValidation.Variety.JSONSchema                  4    5610.61
Update.DocValidation.Array.Compare                       1    1966.4
Update.DocValidation.Array.Compare                       2    4001.03
Update.DocValidation.Array.Compare                       4    6873.1
Update.DocValidation.Array.JSONSchema                    1    1964.63
Update.DocValidation.Array.JSONSchema                    2    4022.3
Update.DocValidation.Array.JSONSchema                    4    6855.32
Update.DocValidation.Nested.Compare                      1    1617.07
Update.DocValidation.Nested.Compare                      2    3024.42
Update.DocValidation.Nested.Compare                      4    5404.98
Update.DocValidation.Nested.JSONSchema                   1    1523.78
Update.DocValidation.Nested.JSONSchema                   2    2850.94
Update.DocValidation.Nested.JSONSchema                   4    5175.55
MultiUpdate.BigAllDocs.NoIndex                           1       0.406287
MultiUpdate.BigAllDocs.NoIndex                           2       0.64595
MultiUpdate.BigAllDocs.NoIndex                           4       0.921409
MultiUpdate.BigAllDocs.Indexed                           1       0.300208
MultiUpdate.BigAllDocs.Indexed                           2       0.472266
MultiUpdate.BigAllDocs.Indexed                           4       0.399487
MultiUpdate.BigAllDocsMultiChange.NoIndex                1       0.385579
MultiUpdate.BigAllDocsMultiChange.NoIndex                2       0.620294
MultiUpdate.BigAllDocsMultiChange.NoIndex                4       0.955967
MultiUpdate.BigAllDocsMultiChange.Indexed                1       0.266006
MultiUpdate.BigAllDocsMultiChange.Indexed                2       0.449322
MultiUpdate.BigAllDocsMultiChange.Indexed                4       0.652762
MultiUpdate.Contended.AllDocs.NoIndex                    1      11.0861
MultiUpdate.Contended.AllDocs.NoIndex                    2      19.2465
MultiUpdate.Contended.AllDocs.NoIndex                    4      30.1998
MultiUpdate.Contended.AllDocs.Indexed                    1       8.38458
MultiUpdate.Contended.AllDocs.Indexed                    2      14.8941
MultiUpdate.Contended.AllDocs.Indexed                    4      25.0018
Inserts.PartialIndex.FilteredRange                       1    1801.58
Inserts.PartialIndex.FilteredRange                       2    3528.36
Inserts.PartialIndex.FilteredRange                       4    6247.59
Inserts.PartialIndex.NonFilteredRange                    1    1756.34
Inserts.PartialIndex.NonFilteredRange                    2    3531.13
Inserts.PartialIndex.NonFilteredRange                    4    6073.03
Inserts.PartialIndex.FullRange                           1    1894.09
Inserts.PartialIndex.FullRange                           2    3431.82
Inserts.PartialIndex.FullRange                           4    6420.68
Insert.Empty                                             1    1872.36
Insert.Empty                                             2    3506.52
Insert.Empty                                             4    6813.38
Insert.EmptyCapped                                       1    1752.36
Insert.EmptyCapped                                       2    3546.53
Insert.EmptyCapped                                       4    5445.73
Insert.EmptyCapped.SeqIntID                              1    1775.37
Insert.EmptyCapped.SeqIntID                              2    3368.35
Insert.EmptyCapped.SeqIntID                              4    5599.52
Insert.JustID                                            1    1849.29
Insert.JustID                                            2    3516.16
Insert.JustID                                            4    6470.76
Insert.IntVector                                         1     615.756
Insert.IntVector                                         2    1119.3
Insert.IntVector                                         4    1985.32
Insert.SeqIntID.Indexed                                  1    1839.6
Insert.SeqIntID.Indexed                                  2    3575.47
Insert.SeqIntID.Indexed                                  4    5285.52
Insert.IntIDUpsert                                       1    1791.1
Insert.IntIDUpsert                                       2    3314.54
Insert.IntIDUpsert                                       4    6004.85
Insert.JustNum                                           1    1842.88
Insert.JustNum                                           2    3417.04
Insert.JustNum                                           4    6672.74
Insert.JustNumIndexed                                    1    1777.94
Insert.JustNumIndexed                                    2    3608.09
Insert.JustNumIndexed                                    4    6291.29
InsertIndexedStringsSimpleCollation                      1    1841.42
InsertIndexedStringsSimpleCollation                      2    3509.45
InsertIndexedStringsSimpleCollation                      4    5992.58
InsertIndexedStringsNonSimpleCollation                   1    1863.16
InsertIndexedStringsNonSimpleCollation                   2    3312.7
InsertIndexedStringsNonSimpleCollation                   4    6424.19
Insert.UniqueIndex                                       1    1821.42
Insert.UniqueIndex                                       2    3369.66
Insert.UniqueIndex                                       4    6319.95
Insert.UniqueIndexCompound                               1    1806.34
Insert.UniqueIndexCompound                               2    3502.79
Insert.UniqueIndexCompound                               4    5998.72
Insert.UniqueIndexCompoundReverse                        1    1811.05
Insert.UniqueIndexCompoundReverse                        2    3327.51
Insert.UniqueIndexCompoundReverse                        4    6113.46
Insert.LargeDocVector                                    1     244.597
Insert.LargeDocVector                                    2     450.711
Insert.LargeDocVector                                    4     824.051
MultiUpdate.Uncontended.SingleDoc.NoIndex                1    1679.93
MultiUpdate.Uncontended.SingleDoc.NoIndex                2    3293.32
MultiUpdate.Uncontended.SingleDoc.NoIndex                4    5891.47
MultiUpdate.Uncontended.SingleDoc.Indexed                1    1662.54
MultiUpdate.Uncontended.SingleDoc.Indexed                2    3293.77
MultiUpdate.Uncontended.SingleDoc.Indexed                4    5469.74
MultiUpdate.Uncontended.TwoDocs.NoIndex                  1    1528.33
MultiUpdate.Uncontended.TwoDocs.NoIndex                  2    2861.64
MultiUpdate.Uncontended.TwoDocs.NoIndex                  4    5083.11
MultiUpdate.Uncontended.TwoDocs.Indexed                  1    1445.17
MultiUpdate.Uncontended.TwoDocs.Indexed                  2    2727.11
MultiUpdate.Uncontended.TwoDocs.Indexed                  4    4880.64
MultiUpdate.Contended.Low.NoIndex                        1    1645.28
MultiUpdate.Contended.Low.NoIndex                        2    3297.33
MultiUpdate.Contended.Low.NoIndex                        4    5703.23
MultiUpdate.Contended.Low.Indexed                        1    1698.03
MultiUpdate.Contended.Low.Indexed                        2    3159.51
MultiUpdate.Contended.Low.Indexed                        4    5403.95
MultiUpdate.Contended.Medium.NoIndex                     1      16.185
MultiUpdate.Contended.Medium.NoIndex                     2      26.8113
MultiUpdate.Contended.Medium.NoIndex                     4      42.2041
MultiUpdate.Contended.Medium.Indexed                     1      12.4412
MultiUpdate.Contended.Medium.Indexed                     2      20.7992
MultiUpdate.Contended.Medium.Indexed                     4      31.9748
MultiUpdate.Contended.Hot.NoIndex                        1     762.417
MultiUpdate.Contended.Hot.NoIndex                        2    1456.96
MultiUpdate.Contended.Hot.NoIndex                        4    2669.37
MultiUpdate.Contended.Hot.Indexed                        1     764.305
MultiUpdate.Contended.Hot.Indexed                        2    1323.07
MultiUpdate.Contended.Hot.Indexed                        4    2244.6
MultiUpdate.Contended.Doc.Seq.NoIndex                    1    1759.87
MultiUpdate.Contended.Doc.Seq.NoIndex                    2    3325.32
MultiUpdate.Contended.Doc.Seq.NoIndex                    4    5625.87
MultiUpdate.Contended.Doc.Seq.Indexed                    1    1741.17
MultiUpdate.Contended.Doc.Seq.Indexed                    2    3260.52
MultiUpdate.Contended.Doc.Seq.Indexed                    4    5501.82
MultiUpdate.Contended.Doc.Rnd.NoIndex                    1    2030.24
MultiUpdate.Contended.Doc.Rnd.NoIndex                    2    4088.09
MultiUpdate.Contended.Doc.Rnd.NoIndex                    4    7321.26
MultiUpdate.Contended.Doc.Rnd.Indexed                    1    2082.05
MultiUpdate.Contended.Doc.Rnd.Indexed                    2    4210.02
MultiUpdate.Contended.Doc.Rnd.Indexed                    4    6972.22
Update.IncNoIndex                                        1    1806.04
Update.IncNoIndex                                        2    3323.54
Update.IncNoIndex                                        4    5999.56
Update.IncWithIndex                                      1    1638.16
Update.IncWithIndex                                      2    3223.59
Update.IncWithIndex                                      4    5501.64
Update.IncNoIndexUpsert                                  1    1689.9
Update.IncNoIndexUpsert                                  2    3417.34
Update.IncNoIndexUpsert                                  4    5621.74
Update.IncWithIndexUpsert                                1    1688.16
Update.IncWithIndexUpsert                                2    3192.15
Update.IncWithIndexUpsert                                4    5532.14
Update.IncFewSmallDoc                                    1    1641.4
Update.IncFewSmallDoc                                    2    3171.71
Update.IncFewSmallDoc                                    4    6026.67
Update.IncFewLargeDoc                                    1    1603.79
Update.IncFewLargeDoc                                    2    3323.27
Update.IncFewLargeDoc                                    4    5533.6
Update.IncFewSmallDocLongFields                          1    1693.68
Update.IncFewSmallDocLongFields                          2    3278.81
Update.IncFewSmallDocLongFields                          4    5564.75
Update.IncFewLargeDocLongFields                          1    1732.16
Update.IncFewLargeDocLongFields                          2    3070.84
Update.IncFewLargeDocLongFields                          4    5745.3
Update.SingleDocFieldAtOffset                            1    2534.46
Update.SingleDocFieldAtOffset                            2    4695.69
Update.SingleDocFieldAtOffset                            4    8110.35
Update.FieldAtOffset                                     1     139.844
Update.FieldAtOffset                                     2     280.418
Update.FieldAtOffset                                     4     558.89
Update.ManyElementsWithinArray                           1     376.624
Update.ManyElementsWithinArray                           2     670.678
Update.ManyElementsWithinArray                           4    1215.78
Update.MatchedElementWithinArray                         1     950.299
Update.MatchedElementWithinArray                         2    1769.31
Update.MatchedElementWithinArray                         4    3203.8
Update.UniqueIndex                                       1    1694.82
Update.UniqueIndex                                       2    3061.11
Update.UniqueIndex                                       4    5579.77
Update.UniqueIndexCompoundReverse                        1    1627.29
Update.UniqueIndexCompoundReverse                        2    2950.91
Update.UniqueIndexCompoundReverse                        4    5678.36
Update.MmsIncShallow1                                    1    1390.51
Update.MmsIncShallow1                                    2    3076.12
Update.MmsIncShallow1                                    4    4770.97
Update.MmsIncShallow2                                    1    1598.69
Update.MmsIncShallow2                                    2    3059.74
Update.MmsIncShallow2                                    4    4702.63
Update.MmsIncDeep1                                       1    1623.32
Update.MmsIncDeep1                                       2    2959.05
Update.MmsIncDeep1                                       4    4681.68
Update.MmsIncDeepSharedPath2                             1    1493.95
Update.MmsIncDeepSharedPath2                             2    2976.49
Update.MmsIncDeepSharedPath2                             4    4499.63
Update.MmsIncDeepSharedPath3                             1    1513.34
Update.MmsIncDeepSharedPath3                             2    3048.57
Update.MmsIncDeepSharedPath3                             4    4399.72
Update.MmsIncDeepDistinctPath2                           1    1581.78
Update.MmsIncDeepDistinctPath2                           2    2986.09
Update.MmsIncDeepDistinctPath2                           4    4520.75
Update.MmsIncDeepDistinctPath3                           1    1501.67
Update.MmsIncDeepDistinctPath3                           2    3013.07
Update.MmsIncDeepDistinctPath3                           4    4341
Update.MmsIncDeepDistinctPath4                           1    1444.53
Update.MmsIncDeepDistinctPath4                           2    3123.42
Update.MmsIncDeepDistinctPath4                           4    4282.16
Update.MmsSetDeepDistinctPaths                           1    1454.77
Update.MmsSetDeepDistinctPaths                           2    2709.53
Update.MmsSetDeepDistinctPaths                           4    4103.17
```