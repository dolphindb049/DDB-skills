# 函数分类

DolphinDB 的函数按照功能可以分为以下类别：

## 数据操作

* **数据类型与转换：**[array](a/array.md), [arrayVector](a/arrayVector.md),
  [bigarray](b/bigarray.md), [blob](b/blob.md), [bool](b/bool.md), [cast](c/cast.md), [ceil](c/ceil.md),
  [char](c/char.md), [complex](c/complex.md), [date](d/date.md), [datehour](d/datehour.md), [datetime](d/datetime.md), [decimal32](d/decimal32.md), [decimal64](d/decimal64.md), [decimal128](d/decimal128.md), [decimalFormat](d/decimalFormat.md), [decimalMultiply](d/decimalMultiply.md),
  [deg2rad](d/deg2rad.md), [dict](d/dict.md), [double](d/double.md), [duration](d/duration.md), [enlist](e/enlist.md), [fixedLengthArrayVector](f/fixedLengthArrayVector.md),
  [floor](f/floor.md), [form](f/form.md), [format](f/format.md), [fromJson](f/fromJson.md), [fromStdJson](f/fromStdJson.md), [hex](h/hex.md), [highDouble](h/highDouble.md),
  [highLong](h/highlong.md), [indexedSeries](i/indexedSeries.md), [int](i/int.md), [int128](i/int128.md),
  [ipaddr](i/ipaddr.md), [isIndexedMatrix](i/isIndexedMatrix.md), [isIndexedSeries](i/isIndexedSeries.md), [isOrderedDict](i/isOrderedDict.md), [jsonExtract](j/jsonextract.md), [long](l/long.md), [lowDouble](l/lowDouble.md), [lowLong](l/lowlong.md), [makeKey](m/makeKey.md), [makeSortedKey](m/makeSortedKey.md)**,**
  [matrix](m/matrix.md), [minute](m/minute.md), [month](m/month.md), [nanotime](n/nanotime.md), [nanotimestamp](n/nanotimestamp.md), [pair](p/pair.md), [parseInt](p/parseInt.md), [parseInteger](p/parseInteger.md),
  [parsejsonTable](p/parsejsontable.md), [point](p/point.md),
  [rad2deg](r/rad2deg.md), [reverse](r/reverse.md), [round](r/round.md), [second](s/second.md), [seq](s/seq.md),
  [set](s/set.md), [setIndexedMatrix!](s/setIndexedMatrix_.md), [setIndexedSeries!](s/setIndexedSeries_.md), [short](s/short.md), [string](s/string.md), [subtuple](s/subtuple.md), [symbol](s/symbol.md), [symbolCode](s/symbolCode.md), [syncDict](s/syncDict.md), [temporalFormat](t/temporalFormat.md), [temporalParse](t/temporalParse.md), [tensor](t/tensor.md), [time](t/time.md), [timestamp](t/timestamp.md), [toJson](t/toJson.md), [toStdJson](t/toStdJson.md), [transpose](t/transpose.md)/[flip](f/flip.md), [type](t/type.md), [typestr](t/typestr.md), [uuid](u/uuid.md)
* **生成：**
  [eye](e/eye.md), [panel](p/panel.md),
  [rollingPanel](r/rollingPanel.md), [seq](s/seq.md), [stretch](s/stretch.md), [take](t/take.md), [til](t/til.md)
* **追加：**[append!](a/append%21.md)/[push!](p/push_.md), [appendTuple!](a/appendTupel_.md), [memberModify!](m/membermodify.md)
* **删除、清理：**[clear!](c/clear_.md), [drop](d/drop.md), [dropna](d/dropna.md), [erase!](e/erase_.md), [pop!](p/pop_.md), [removeHead!](r/removeHead_.md), [removeTail!](r/removeTail_.md)
* **查找：**[at](a/at.md), [binsrch](b/binsrch.md), [cell](c/cell.md), [cells](c/cells.md), [col](c/col.md),
  [eachAt(@)](../progr/operators/eachAt.md), [find](f/find.md), [first](f/first.md),
  [firstHit](f/firstHit.md), [firstNot](f/firstNot.md), [head](h/head.md), [ifirstHit](i/ifirstHit.md), [ifirstNot](i/ifirstNot.md), [ilastNot](i/ilastNot.md), [last](l/last.md), [lastNot](l/lastNot.md), [loc](l/loc.md), [milastNot](m/milastNot.md), [row](r/row.md), [searchK](s/searchK.md), [slice](s/slice.md), [sliceByKey](s/sliceByKey.md), [subarray](s/subarray.md), [tail](t/tail.md)
* **排序：**[denseRank](d/denseRank.md), [isort](i/isort.md), [isort!](i/isort_.md), [isortTop](i/isortTop.md), [isSorted](i/isSorted.md), [rank](r/rank.md), [sort](s/sort.md), [sort!](s/sort_.md), [sortBy!](s/sortBy_.md)
* **空值查找、填充：**[bfill!](b/bfill_.md), [ffill](f/ffill.md), [ffill!](f/ffill_.md), [fill!](f/fill_.md), [hasNull](h/hasNull.md), [ifNull](i/ifNull.md), [ifValid](i/ifValid.md), [interpolate](i/interpolate.md), [isNanInf](i/isNanInf.md), [isNothing](i/isNothing.md), [isNull](i/isNull.md), [isValid](i/isValid.md), [isVoid](i/isVoid.md), [lfill](l/lfill.md), [lfill!](l/lfill_.md), [nanInfFill](n/nanInfFill.md), [nullFill](n/nullFill.md), [nullFill!](n/nullFill_.md)
* **替换：**[replace](r/replace.md), [replace!](r/replace_.md)
* **移动：**[lshift](l/lshift.md), [move](m/move.md), [next](n/next.md), [nextState](n/nextState.md), [prev](p/prev.md), [prevState](p/prevState.md), [rshift](r/rshift.md)
* **合并：**[concatMatrix](c/concatMatrix.md), [join](j/join.md), [join!](j/join%21.md), [merge](m/merge.md), [union](u/union.md), [unionAll](u/unionAll.md)
* **分割：**[cut](c/cut.md)
* **过滤：**[conditionalFilter](c/conditionalFilter.md)
* **对齐：**[align](a/align.md)
* **展开、重组：**[flatten](f/flatten.md), [regroup](r/regroup.md), [reshape](r/reshape.md), [shuffle](s/shuffle.md), [shuffle!](s/shuffle_.md), [ungroup](u/ungroup.md)
* **分组：**[bar](b/bar.md), [bucket](b/bucket.md), [cutPoints](c/cutPoints.md), [dailyAlignedBar](d/dailyAlignedBar.md), [digitize](d/digitize.md), [groups](g/groups.md),
  [segment](s/segment.md), [volumeBar](v/volumeBar.md)
* **加载：**[loadNpy](l/loadNpy.md), [loadNpz](l/loadNpz.md), [loadRecord](l/loadRecord.md), [loadTable](l/loadTable.md),
  [loadText](l/loadText.md), [loadTextEx](l/loadTextEx.md), [ploadText](p/ploadText.md)
* **编码转换：**[base64Decode](b/base64Decode.md), [base64Encode](b/base64Encode.md), [compress](c/compress.md), [decodeShortGenomeSeq](d/decodeShortGenomeSeq.md),
  [decompress](d/decompress.md), [encodeShortGenomeSeq](e/encodeShortGenomeSeq.md),
  [genShortGenomeSeq](g/genShortGenomeSeq.md),
  [oneHot](o/oneHot.md), [pack](p/pack.md), [rdp](r/rdp.md), [unpack](u/unpack.md)
* **累积窗口：**[cumavg](c/cumavg.md), [cumbeta](c/cumbeta.md), [cumcorr](c/cumcorr.md), [cumcount](c/cumcount.md), [cumcovar](c/cumcovar.md), [cumfirstNot](c/cumfirstNot.md), [cumlastNot](c/cumlastNot.md), [cummax](c/cummax.md), [cummed](c/cummed.md), [cummin](c/cummin.md), [cumnunique](c/cumnunique.md), [cumpercentile](c/cumpercentile.md), [cumPositiveStreak](c/cumPositiveStreak.md), [cumprod](c/cumprod.md),
  [cumrank](c/cumrank.md), [cumstd](c/cumstd.md), [cumstdp](c/cumstdp.md), [cumsum](c/cumsum.md), [cumsum2](c/cumsum2.md), [cumsum3](c/cumsum3.md), [cumsum4](c/cumsum4.md), [cumvar](c/cumvar.md), [cumvarp](c/cumvarp.md), [cumwavg](c/cumwavg.md), [cumwsum](c/cumwsum.md), [dynamicGroupCumsum](d/dynamicGroupCumsum.md), [dynamicGroupCumcount](d/dynamicGroupCumcount.md)
* **m 系列：**[mavg](m/mavg.md), [mbeta](m/mbeta.md), [mcorr](m/mcorr.md), [mcount](m/mcount.md), [mcovar](m/mcovar.md), [mfirst](m/mfirst.md), [mfirstNot](m/mifirstNot.md), [mifirstNot](m/mifirstNot.md), [milastNot](m/milastNot.md), [mimax](m/mimax.md), [mimin](m/mimin.md), [mkurtosis](m/mkurtosis.md), [mlast](m/mlast.md), [mlastNot](m/mlastnot.md), [mLowRange](m/mlowrange.md), [mmad](m/mmad.md), [mmax](m/mmax.md), [mmaxPositiveStreak](m/mmaxPositiveStreak.md), [mmed](m/mmed.md), [mmin](m/mmin.md), [mmse](m/mmse.md),
  [movingTopNIndex](m/movingTopNIndex.md), [movingWindowIndex](m/movingWindowIndex.md), [mpercentile](m/mpercentile.md), [mprod](m/mprod.md), [mrank](m/mrank.md), [mskew](m/mskew.md), [mslr](m/mslr.md),
  [mstd](m/mstd.md), [mstdp](m/mstdp.md), [msum](m/msum.md), [msum2](m/msum2.md), [mTopRange](m/mtoprange.md), [mvar](m/mvar.md), [mvarp](m/mvarp.md),
  [mwavg](m/mwavg.md), [mwsum](m/mwsum.md)
* **tm 系列：**[tmavg](t/tmavg.md), [tmbeta](t/tmbeta.md), [tmcorr](t/tmcorr.md), [tmcount](t/tmcount.md), [tmcovar](t/tmcovar.md), [tmfirst](t/tmfirst.md), [tmkurtosis](t/tmkurtosis.md), [tmlast](t/tmlast.md), [tmLowRange](t/tmlowrange.md),
  [tmmax](t/tmmax.md), [tmmed](t/tmmed.md), [tmmin](t/tmmin.md), [tmpercentile](t/tmpercentile.md), [tmprod](t/tmprod.md), [tmrank](t/tmrank.md), [tmskew](t/tmskew.md), [tmstd](t/tmstd.md), [tmstdp](t/tmstdp.md), [tmsum](t/tmsum.md), [tmsum2](t/tmsum2.md), [tmTopRange](t/tmtoprange.md),
  [tmvar](t/tmvar.md), [tmvarp](t/tmvarp.md), [tmwavg](t/tmwavg.md), [tmwsum](t/tmwsum.md)
* **mTopN：**[mavgTopN](m/mavgTopN.md), [mbetaTopN](m/mbetaTopN.md), [mcorrTopN](m/mcorrTopN.md), [mcovarTopN](m/mcovarTopN.md),
  [mpercentileTopN](m/mpercentiletopn.md), [mstdpTopN](m/mstdpTopN.md), [mstdTopN](m/mstdTopN.md), [msumTopN](m/msumTopN.md), [mvarpTopN](m/mvarpTopN.md), [mvarTopN](m/mvarTopN.md), [mwsumTopN](m/mwsumTopN.md),
* **row 系列：**[rowAlign](r/rowAlign.md), [rowAnd](r/rowAnd.md),
  [rowAt](r/rowAt.md), [rowAvg](r/rowAvg.md), [rowBeta](r/rowBeta.md), [rowCorr](r/rowCorr.md), [rowCount](r/rowCount.md), [rowCovar](r/rowCovar.md), [rowDenseRank](r/rowDenseRank.md), [rowDot](r/rowDot.md), [rowEuclidean](r/rowEuclidean.md), [rowGmd5](r/rowgmd5.md), [rowImax](r/rowImax.md), [rowImin](r/rowImin.md), [rowKurtosis](r/rowKurtosis.md),
  [rowMax](r/rowMax.md), [rowMin](r/rowMin.md), [rowMove](r/rowMove.md), [rowNext](r/rowNext.md), [rowOr](r/rowOr.md), [rowPrev](r/rowPrev.md), [rowProd](r/rowProd.md), [rowRank](r/rowRank.md), [rowSize](r/rowSize.md), [rowSkew](r/rowSkew.md), [rowStd](r/rowStd.md), [rowStdp](r/rowStdp.md), [rowSum](r/rowSum.md), [rowSum2](r/rowSum2.md), [rowTanimoto](r/rowTanimoto.md),
  [rowVar](r/rowVar.md), [rowVarp](r/rowVarp.md), [rowWavg](r/rowWavg.md), [rowWsum](r/rowWsum.md), [rowXor](r/rowXor.md)
* **TA-lib 系列：**[dema](d/dema.md), [ema](e/ema.md), [gema](g/gema.md),
  [kama](k/kama.md), [linearTimeTrend](l/linearTimeTrend.md), [ma](m/ma.md), [sma](s/sma.md), [t3](t/t3.md), [tema](t/tema.md), [trima](t/trima.md), [wilder](w/wilder.md), [wma](w/wma.md)
* **字符串：**[charAt](c/charAt.md), [concat](c/concat.md), [convertEncode](c/convertEncode.md), [crc32](c/crc32.md), [endsWith](e/endsWith.md), [fromUTF8](f/fromUTF8.md), [gmd5](g/gmd5.md), [ilike](i/ilike.md), [initcap](i/initcap.md), [isAlNum](i/isAlNum.md), [isAlpha](i/isAlpha.md), [isDigit](i/isDigit.md), [isLower](i/isLower.md), [isNumeric](i/isNumeric.md), [isSpace](i/isSpace.md), [isTitle](i/isTitle.md), [isUpper](i/isUpper.md), [left](l/left.md), [like](l/like.md), [lower](l/lower.md),
  [lpad](l/lpad.md), [ltrim](l/ltrim.md), [md5](m/md5.md), [regexCount](r/regexCount.md), [regexFind](r/regexFind.md), [regexFindStr](r/regexfindstr.md), [regexReplace](r/regexReplace.md), [repeat](r/repeat.md), [right](r/right.md), [rpad](r/rpad.md), [rtrim](r/rtrim.md), [split](s/split.md), [startsWith](s/startsWith.md), [stringFormat](s/stringFormat.md), [strip](s/strip.md), [strlen](s/strlen.md), [strlenu](s/strlenu.md), [strpos](s/strpos.md), [strReplace](s/strReplace.md), [substr](s/substr.md), [substru](s/substru.md), [toCharArray](t/toCharArray.md), [toUTF8](t/toUTF8.md), [trim](t/trim.md), [upper](u/upper.md)
* **时间处理：**[addMarketHoliday](a/addMarketHoliday.md),
  [asFreq](a/asFreq.md), [businessDay](b/businessDay.md), [businessMonthBegin](b/businessMonthBegin.md), [businessMonthEnd](b/businessMonthEnd.md), [businessQuarterBegin](b/businessQuarterBegin.md), [businessQuarterEnd](b/businessQuarterEnd.md), [businessYearBegin](b/businessYearBegin.md), [businessYearEnd](b/businessYearEnd.md), [concatDateTime](c/concatDateTime.md), [convertTZ](c/convertTZ.md), [date](d/date.md), [dayOfMonth](d/dayOfMonth.md), [dayOfWeek](d/dayOfWeek.md), [dayOfYear](d/dayOfYear.md), [daysInMonth](d/daysInMonth.md),
  [fy5253](f/fy5253.md), [fy5253Quarter](f/fy5253Quarter.md), [getMarketCalendar](g/getMarketCalendar.md), [gmtime](g/gmtime.md), [hour](h/hour.md), [hourOfDay](h/hourOfDay.md), [isLeapYear](i/isLeapYear.md), [isMonthEnd](i/isMonthEnd.md), [isMonthStart](i/isMonthStart.md), [isQuarterEnd](i/isQuarterEnd.md), [isQuarterStart](i/isQuarterStart.md), [isYearEnd](i/isYearEnd.md), [isYearStart](i/isYearStart.md), [lastWeekOfMonth](l/lastWeekOfMonth.md), [listAllMarkets](l/listAllMarkets.md), [localtime](l/localtime.md), [microsecond](m/microsecond.md), [millisecond](m/millisecond.md), [minuteOfHour](m/minuteOfHour.md), [month](m/month.md), [monthBegin](m/monthBegin.md), [monthEnd](m/monthEnd.md), [monthOfYear](m/monthOfYear.md), [nanosecond](n/nanosecond.md), [now](n/now.md), [quarterBegin](q/quarterBegin.md), [quarterEnd](q/quarterEnd.md), [secondOfMinute](s/secondOfMinute.md), [semiMonthBegin](s/semiMonthBegin.md), [semiMonthEnd](s/semiMonthEnd.md), [temporalAdd](t/temporalAdd.md), [temporalDeltas](t/temporalDeltas.md), [temporalDiff](t/temporalDiff.md), [temporalSeq](t/temporalSeq.md), [today](t/today.md), [transFreq](t/transFreq.md), [updateMarketHoliday](u/updateMarketHoliday.md), [weekBegin](w/weekBegin.md), [weekday](w/weekday.md), [weekEnd](w/weekEnd.md), [weekOfMonth](w/weekOfMonth.md), [weekOfYear](w/weekOfYear.md), [year](y/year.md), [yearBegin](y/yearBegin.md), [yearEnd](y/yearEnd.md)

## 数据库/数据表

* **库表操作：**[addColumn](a/addColumn.md), [addFunctionView](a/addFunctionView.md), [addRangePartitions](a/addRangePartitions.md), [addValuePartitions](a/addValuePartitions.md), [backup](b/backup.md), [backupDB](b/backupDB.md), [backupTable](b/backupTable.md),
  [cacheDS!](c/cacheDS_.md), [cacheDSNow](c/cacheDSNow.md), [cachedTable](c/cachedTable.md), [checkBackup](c/checkBackup.md), [clearAllTSDBSymbolBaseCache](c/clearalltsdbsymbolbasecache.md), [clearDSCache!](c/clearDSCache_.md), [clearDSCacheNow](c/clearDSCacheNow.md), [columnNames](c/columnNames.md), [createDimensionTable](c/createdimensiontable.md), [createDistributedInMemoryTable](c/createDistributedInMemoryTable.md), [createIPCInMemoryTable](c/createIPCInMemoryTable.md),
  [createPartitionedTable](c/createPartitionedTable.md), [createTable](c/createTable.md), [database](d/database.md), [disableActivePartition](d/disableActivePartition.md),
  [disableQueryMonitor](d/disableQueryMonitor.md), [disableTSDBAsyncSorting](d/disableTSDBAsyncSorting.md), [dropColumns!](d/dropColumns_.md), [dropDatabase](d/dropDatabase.md), [dropDistributedInMemoryTable](d/dropDistributedInMemoryTable.md), [dropFunctionView](d/dropFunctionView.md), [dropIPCInMemoryTable](d/dropIPCInMemoryTable.md), [dropPartition](d/dropPartition.md), [dropTable](d/dropTable.md), [enableActivePartition](e/enableActivePartition.md), [enableQueryMonitor](e/enableQueryMonitor.md), [enableTSDBAsyncSorting](e/enableTSDBAsyncSorting.md), [existsDatabase](e/existsDatabase.md), [existsPartition](e/existsPartition.md), [existsTable](e/existsTable.md), [extractTextSchema](e/extractTextSchema.md), [flushOLAPCache](f/flushOLAPCache.md), [flushTSDBCache](f/flushTSDBCache.md), [getAllDBGranularity](g/getAllDBGranularity.md), [getAllDBs](g/getAllDBs.md), [getBackupList](g/getBackupList.md), [getBackupMeta](g/getBackupMeta.md), [getBackupStatus](g/getBackupStatus.md), [getChunkPath](g/getChunkPath.md), [getChunksMeta](g/getChunksMeta.md), [getClusterChunksStatus](g/getClusterChunksStatus.md), [getClusterDFSDatabases](g/getClusterDFSDatabases.md),
  [getClusterDFSTables](g/getClusterDFSTables.md),
  [getConfigure](g/getConfigure.md)/[getConfig](g/getConfig.md), [getDFSDatabases](g/getDFSDatabases.md), [getDFSDatabasesByOwner](g/getdfsdatabasebyowner.md), [getDFSTablesByDatabase](g/getDFSTablesByDatabase.md),
  [getFunctionViews](g/getFunctionViews.md), [getLevelFileIndexCacheStatus](g/getLevelFileIndexCacheStats.md), [getLocalIOTDBStaticTable](g/getLocalIOTDBStaticTable.md),
  [getMemLimitOfQueryResult](g/getMemLimitOfQueryResult.md), [getMemLimitOfTaskGroupResult](g/getMemLimitOfTaskGroupResult.md), [getOLAPCacheEngineSize](g/getOLAPCacheEngineSize.md),
  [getOLAPCacheEngineStat](g/getOLAPCacheEngineStat.md), [getOLAPCachedSymbolBaseMemSize](g/getOLAPCachedSymbolBaseMemSize.md),
  [getPKEYCompactionTaskStatus](g/getpkeycompactiontaskstatus.md), [getPKEYMetaData](g/getpkeymetadata.md),
  [getRecoveryTaskStatus](g/getRecoveryTaskStatus.md),
  [getRecoveryWorkerNum](g/getRecoveryWorkerNum.md),
  [getRedoLogGCStat](g/getRedoLogGCStat.md), [getTables](g/getTables.md), [getTablet](g/getTablet.md), [getTabletsMeta](g/getTabletsMeta.md), [getTransactionStatus](g/getTransactionStatus.md), [getTSDBCachedSymbolBaseMemSize](g/getTSDBCachedSymbolBaseMemSize.md), [getTSDBCacheEngineSize](g/getTSDBCacheEngineSize.md),
  [getTSDBCompactionTaskStatus](g/getTSDBCompactionTaskStatus.md), [getTSDBMetaData](g/getTSDBMetaData.md), [getUnresolvedTxn](g/getUnresolvedTxn.md), [imr](i/imr.md), [indexedTable](i/indexedTable.md), [keyedTable](k/keyedTable.md),
  [latestIndexedTable](l/latestIndexedTable.md), [latestKeyedStreamTable](l/latestkeyedstreamtable.md),
  [latestKeyedTable](l/latestKeyedTable.md), [loadBackup](l/loadBackup.md), [loadDistributedInMemoryTable](l/loadDistributedInMemoryTable.md), [loadIPCInMemoryTable](l/loadIPCInMemoryTable.md), [loadMvccTable](l/loadMvccTable.md), [loadTableBySQL](l/loadTableBySQL.md), [migrate](m/migrate.md), [mr](m/mr.md),
  [multiTableRepartitionDS](m/multiTableRepartitionDS.md), [mvccTable](m/mvccTable.md), [purgeCacheEngine](p/purgeCacheEngine.md), [rename!](r/rename_.md),
  [renameTable](r/renameTable.md), [reorderColumns!](r/reorderColumns_.md), [repartitionDS](r/repartitionDS.md), [replaceColumn!](r/replaceColumn_.md), [replay](r/replay.md), [replayDS](r/replayDS.md), [resetRecoveryWorkerNum](r/resetRecoveryWorkerNum.md), [restore](r/restore.md), [restoreDB](r/restoreDB.md), [restoreTable](r/restoreTable.md), [rowNames](r/rowNames.md), [rowNo](r/rowNo.md), [saveDatabase](s/saveDatabase.md),
  [saveDualPartition](s/saveDualPartition.md), [savePartition](s/savePartition.md), [saveTable](s/saveTable.md), [schema](s/schema.md), [setAtomicLevel](s/setAtomicLevel.md), [setChunkLastUpdateTime](s/setChunkLastUpdateTime.md), [setColumnComment](s/setColumnComment.md), [setMaxBlockSizeForReservedMemory](s/setMaxBlockSizeForReservedMemory.md), [setMaxConnections](s/setMaxConnections.md), [setMaxMemSize](s/setMaxMemSize.md), [setMemLimitOfQueryResult](s/setMemLimitOfQueryResult.md),
  [setMemLimitOfTaskGroupResult](s/setMemLimitOfTaskGroupResult.md), [setMemLimitOfTempResult](s/setMemLimitOfTempResult.md), [setOLAPCacheEngineSize](s/setOLAPCacheEngineSize.md),
  [setReservedMemSize](s/setReservedMemSize.md),
  [setTableComment](s/settablecomment.md), [setTSDBCacheEngineSize](s/setTSDBCacheEngineSize.md), [sqlDS](s/sqlDS.md), [table](t/table.md), [tableInsert](t/tableInsert.md), [tableUpsert](t/tableUpsert.md), [textChunkDS](t/textChunkDS.md), [transDS!](t/transDS_.md), [triggerTSDBCompaction](t/triggerTSDBCompaction.md),
  [truncate](t/truncate.md), [tupleSum](t/tupleSum.md), [update!](u/update_.md), [upsert!](u/upsert_.md)
* **catalog相关操作：**[createCatalog](c/createCatalog.md), [createSchema](c/createSchema.md), [dropCatalog](d/dropCatalog.md), [dropSchema](d/dropSchema.md), [existsCatalog](e/existsCatalog.md), [getAllCatalogs](g/getAllCatalogs.md), [getCurrentCatalog](g/getCurrentCatalog.md), [getSchemaByCatalog](g/getSchemaByCatalog.md), [renameCatalog](r/renameCatalog.md), [renameSchema](r/renameSchema.md), [setDefaultCatalog](s/setDefaultCatalog.md)
* **集群操作：**[addNode](a/addNode.md), [addVolumes](a/addVolumes.md), [cancelRecoveryTask](c/cancelRecoveryTask.md), [copyReplicas](c/copyReplicas.md), [deleteReplicas](d/deleteReplicas.md), [getActiveMaster](g/getActiveMaster.md), [getActiveMaster](g/getActiveMaster.md), [getConnections](g/getConnections.md), [getDatabaseClusterReplicationStatus](g/getDatabaseClusterReplicationStatus.md), [getMasterReplicationStatus](g/getMasterReplicationStatus.md), [getNodeAlias](g/getNodeAlias.md), [getNodeHost](g/getNodeHost.md), [getNodePort](g/getNodePort.md),
  [getNodeType](g/getNodeType.md), [getRecentSlaveReplicationInfo](g/getRecentSlaveReplicationInfo.md), [getSlaveReplicationStatus](g/getSlaveReplicationStatus.md), [getSlaveReplicationQueueStatus](g/getslavereplicationqueuestatus.md),
  [isControllerInitialized](i/isControllerInitialized.md),
  [isDataNodeInitialized](i/isDataNodeInitialized.md),
  [moveChunksAcrossVolume](m/moveChunksAcrossVolume.md), [moveReplicas](m/moveReplicas.md), [pnodeRun](p/pnodeRun.md),
  [rebalanceChunksAmongDataNodes](r/rebalanceChunksAmongDataNodes.md), [rebalanceChunksWithinDataNode](r/rebalanceChunksWithinDataNode.md), [remoteRun](r/remoteRun.md), [remoteRunCompatible](r/remoteruncompatible.md), [remoteRunWithCompression](r/remoteRunWithCompression.md),
  [removeNode](r/removenode.md), [resetDBDirMeta](r/resetDBDirMeta.md), [restoreDislocatedTablet](r/restoreDislocatedTablet.md),
  [resumeRecovery](r/resumeRecovery.md), [rpc](r/rpc.md), [setDatabaseForClusterReplication](s/setDatabaseForClusterReplication.md), [setTimeoutTick](s/setTimeoutTick.md), [skipClusterReplicationTask](s/skipClusterReplicationTask.md), [startClusterReplication](s/startClusterReplication.md),
  [startDataNode](s/startDataNode.md), [stopClusterReplication](s/stopClusterReplication.md),
  [stopDataNode](s/stopDataNode.md), [suspendRecovery](s/suspendRecovery.md), [triggerNodeReport](t/triggerNodeReport.md), [xdb](x/xdb.md)
* **多集群操作：**[getAllClusters](g/getAllClusters.md), [getCatalogsByCluster](g/getCatalogsByCluster.md), [getClusterStatus](g/getClusterStatus.md), [getDatabasesByCluster](g/getDatabasesByCluster.md), [getGroupAccessByCluster](g/getGroupAccessByCluster.md),
  [getGroupListOfAllClusters](g/getGroupListOfAllClusters.md), [getSchemasByCluster](g/getSchemasByCluster.md), [getTableAccessByCluster](g/getTableAccessByCluster.md),
  [getTablesByCluster](g/getTablesByCluster.md), [getTablesOfAllClusters](g/getTablesOfAllClusters.md),
  [getTableSchemaByCluster](g/getTableSchemaByCluster.md), [getUserAccessByCluster](g/getUserAccessByCluster.md),
  [getUserListOfAllClusters](g/getUserListOfAllClusters.md), [listPluginsByCluster](l/listPluginsByCluster.md)
* **计算组相关操作：**[clearComputeNodeCache](c/clearcomputenodecache.md), [clearComputeNodeDiskCache](c/clearcomputenodediskcache.md), [flushComputeNodeMemCache](f/flushcomputenodememcache.md),
  [getComputeGroupChunksStatus](g/getcomputegroupchunksstatus.md), [getComputeNodeCacheDetails](g/getComputeNodeCacheDetails.md), [getComputeNodeCacheStat](g/getcomputenodecachestat.md),
  [getComputeNodeCacheWarmupJobStatus](g/getcomputenodecachewarmupjobstatus.md), [getComputeNodeCachingDelay](g/getcomputenodecachingdelay.md), [getPrefetchComputeNodeData](g/getprefetchcomputenodedata.md), [setComputeNodeCachingDelay](s/setcomputenodecachingdelay.md), [setPrefetchComputeNodeData](s/setprefetchcomputenodedata.md), [warmupComputeNodeCache](w/warmupcomputenodecache.md)

## SQL

* **关键字：**[alter](../progr/sql/alter.md), [any/all](../progr/sql/any.md), [between](../progr/sql/between.md), [case](../progr/sql/case.md), [cgroup by](../progr/sql/cgroupby.md), [coalesce](../progr/sql/coalesce.md), [context by](../progr/sql/contextBy.md), [create](../progr/sql/create.md), [delete](../progr/sql/delete.md), [distinct](../progr/sql/distinct.md), [drop](../progr/sql/drop.md), [exec](../progr/sql/exec.md), [exists](../progr/sql/exists.md), [group by](../progr/sql/groupby.md), [having](../progr/sql/having.md), [[HINT\_EXPLAIN](../progr/sql/hint_explain.md)], [in](../progr/sql/in.md), [insert into](../progr/sql/insertInto.md), [interval](../progr/sql/interval.md), [is null](../progr/sql/isnull.md),
  [like/LIKE](../progr/sql/like.md), [limit](../progr/sql/limit.md), [map](../progr/sql/map.md), [notBetween/NOTBETWEEN](../progr/sql/notbetween.md), [notIn/NOTIN](../progr/sql/notin.md), [notLike/NOTLIKE](../progr/sql/notlike.md), [nullIf](n/nullIf.md), [order by](../progr/sql/orderby.md), [partition](../progr/sql/partition.md), [pivot by](../progr/sql/pivotBy.md), [sample](../progr/sql/sample.md), [select](../progr/sql/Select.md), [SQL Trace](../progr/sql/sql_trace.md), [top](../progr/sql/top.md), [union/union all](../progr/sql/union.md), [unpivot](u/unpivot.md), [update](../progr/sql/update.md), [where](../progr/sql/where.md), [with](../progr/sql/with.md)
* **表连接：**[aj](../progr/sql/asofjoin.md), [cj](../progr/sql/crossjoin.md), [ej](../progr/sql/equijoin.md), [fj](../progr/sql/fulljoin.md) (full join), [inner join](../progr/sql/innerjoin.md), [lj](../progr/sql/leftjoin.md) (left join), [lsj](../progr/sql/leftjoin.md) (left semi join), [pj](../progr/sql/prefixjoin.md), [pwj](../progr/sql/windowjoin.md), [right join](../progr/sql/rightjoin.md),
  [sej](../progr/sql/equijoin.md), [wj](../progr/sql/windowjoin.md)
* **状态查看：**[getCompletedQueries](g/getCompletedQueries.md), [getQueryStatus](g/getQueryStatus.md), [getRunningQueries](g/getRunningQueries.md), [getTraces](../progr/sql/getTraces.md), [setTraceMode](../progr/sql/setTraceMode.md), [viewTraceInfo](../progr/sql/viewTraceInfo.md)

## 数学和统计

* **数学：**[abs](a/abs.md), [acos](a/acos.md), [acosh](a/acosh.md), [add](a/add.md), [asin](a/asin.md),
  [asinh](a/asinh.md), [atan](a/atan.md), [atanh](a/atanh.md), [cbrt](c/cbrt.md), [clip](c/clip.md),
  [clip!](c/clip_.md), [cos](c/cos.md), [cosh](c/cosh.md), [cholesky](c/cholesky.md), [derivative](d/derivative.md), [diag](d/diag.md), [div](d/div.md), [det](d/det.md), [eig](e/eig.md), [exp](e/exp.md), [exp2](e/exp2.md), [expm1](e/expm1.md),
  [gram](g/gram.md), [gramSchmidt](g/gramSchmidt.md), [integral](i/integral.md), [inverse](i/inverse.md), [intersection](i/intersection.md), [iterate](i/iterate.md), [log](l/log.md), [log1p](l/log1p.md),
  [log2](l/log2.md), [log10](l/log10.md), [lu](l/lu.md), [mod](m/mod.md), [mul](m/mul.md), [neg](n/neg.md), [pow](p/pow.md), [ratio](r/ratio.md), [reciprocal](r/reciprocal.md), [repmat](r/repmat.md), [sin](s/sin.md), [sinh](s/sinh.md),
  [sqrt](s/sqrt.md), [square](s/square.md), [sub](s/sub.md), [symmetricDifference](s/symmetricDifference.md), [svd](s/svd.md), [tan](t/tan.md), [tanh](t/tanh.md), [tril](t/tril.md),
  [triu](t/triu.md), [schur](s/schur.md), [signbit](s/signbit.md), [signum](s/signum.md), [qr](q/qr.md)
* **统计：**[atImax](a/atImax.md), [atImin](a/atImin.md), [avg](a/avg.md),
  [boxcox](b/boxcox.md), [contextSum](c/contextSum.md), [contextSum2](c/contextSum2.md),
  [count](c/count.md), [covar](c/covar.md), [covarMatrix](c/covarMatrix.md), [crossStat](c/crossStat.md), [cubicHermiteSplineFit](c/cubichermitesplinefit.md), [cumnunique](c/cumnunique.md), [demean](d/demean.md), [dot](d/dot.md), [ewmCov](e/ewmCov.md), [ewmMean](e/ewmMean.md), [ewmStd](e/ewmStd.md), [ewmVar](e/ewmVar.md), [gaussianKde](g/gaussiankde.md), [gaussianKdePredict](g/gaussiankdepredict.md), [imax](i/imax.md), [imin](i/imin.md), [kurtosis](k/kurtosis.md), [mad](m/mad.md), [max](m/max.md), [maxIgnoreNull](m/maxignorenull.md), [med](m/med.md), [mean](m/mean.md), [min](m/min.md),
  [minIgnoreNull](m/minignorenull.md), [mode](m/mode.md), [mmed](m/mmed.md),
  [nunique](n/nunique.md), [percentChange](p/percentChange.md), [percentile](p/percentile.md), [percentileRank](p/percentileRank.md), [prod](p/prod.md), [quantile](q/quantile.md), [quantileSeries](q/quantileSeries.md), [rms](r/rms.md),[sem](s/sem.md), [skew](s/skew.md),
  [std](s/std.md), [stdp](s/stdp.md), [summary](s/summary.md), [sum](s/sum.md), [sum2](s/sum2.md),
  [sum3](s/sum3.md), [sum4](s/sum4.md), [stat](s/stat.md), [var](v/var.md), [varp](v/varp.md),
  [wavg](w/wavg.md), [wc](w/wc.md),
  [wcovar](w/wcovar.md), [wsum](w/wsum.md), [histogram2d](h/histogram2d.md), [kroghInterpolateFit](k/kroghinterpolatefit.md), [linearInterpolateFit](l/linearinterpolatefit.md)
* **相关性：**[acf](a/acf.md), [autocorr](a/autocorr.md), [corr](c/corr.md), [corrMatrix](c/corrMatrix.md), [distance](d/distance.md), [ewmCorr](e/ewmCorr.md), [euclidean](e/euclidean.md), [kendall](k/kendall.md), [mutualInfo](m/mutualInfo.md), [rowEuclidean](r/rowEuclidean.md), [rowTanimoto](r/rowTanimoto.md), [spearmanr](s/spearmanr.md), [tanimoto](t/tanimoto.md)
* **序列分析：**[isMonotonicIncreasing](i/isMonotonicIncreasing.md)/[isMonotonic](i/isMonotonic.md), [isMonotonicDecreasing](i/isMonotonicDecreasing.md), [isPeak](i/isPeak.md),
  [isValley](i/isValley.md), [zigzag](z/zigzag.md)
* **机器学习：**[adaBoostClassifier](a/adaBoostClassifier.md), [adaBoostRegressor](a/adaBoostRegressor.md), [beta](b/beta.md), [bvls](b/bvls.md), [elasticNet](e/elasticNet.md), [elasticNetCV](e/elasticNetCV.md), [gaussianNB](g/gaussianNB.md), [glm](g/glm.md), [gmm](g/gmm.md), [kernelRidge](k/kernelRidge.md), [kmeans](k/kmeans.md), [knn](k/knn.md), [lasso](l/lasso.md), [lassoBasic](l/lassoBasic.md), [lassoCV](l/lassoCV.md), [logisticRegression](l/logisticRegression.md), [mmse](m/mmse.md), [msl](m/mslr.md),
  [multinomialNB](m/multinomialNB.md), [ols](o/ols.md), [olsEx](o/olsEx.md),
  [piecewiseLinFit](p/piecewiselinfit.md), [poly1d](p/poly1d.md), [polyPredict](p/polyPredict.md), [polyFit](p/polyfit.md), [polynomial](p/polynomial.md), [predict](p/predict.md), [pwlfPredict](p/pwlfpredict.md),
  [randomForestClassifier](r/randomForestClassifier.md), [randomForestRegressor](r/randomForestRegressor.md), [residual](r/residual.md), [ridge](r/ridge.md), [ridgeBasic](r/ridgeBasic.md), [vectorAR](v/vectorar.md), [wls](w/wls.md), [garch](g/garch.md)
* **分布与假设检验：**[adfuller](a/adfuller.md), [anova](a/anova.md), [cdfBeta](c/cdfBeta.md), [cdfBinomial](c/cdfBinomial.md), [cdfChiSquare](c/cdfChiSquare.md), [cdfExp](c/cdfExp.md), [cdfF](c/cdfF.md), [cdfGamma](c/cdfGamma.md), [cdfKolmogorov](c/cdfKolmogorov.md), [cdfLogistic](c/cdfLogistic.md),
  [cdfNormal](c/cdfNormal.md), [cdfPoisson](c/cdfPoisson.md), [cdfStudent](c/cdfStudent.md), [cdfUniform](c/cdfUniform.md), [cdfWeibull](c/cdfWeibull.md), [cdfZipf](c/cdfZipf.md), [chiSquareTest](c/chiSquareTest.md),
  [coint](c/coint.md),
  [esd](e/esd.md), [fTest](f/fTest.md), [invBeta](i/invBeta.md), [invBinomial](i/invBinomial.md), [invChiSquare](i/invChiSquare.md), [invExp](i/invExp.md), [invF](i/invF.md), [invGamma](i/invGamma.md), [invLogistic](i/invLogistic.md), [invNormal](i/invNormal.md), [invStudent](i/invStudent.md), [invPoisson](i/invPoisson.md),
  [invUniform](i/invUniform.md), [invWeibull](i/invWeibull.md), [ksTest](k/ksTest.md), [mannWhitneyUTest](m/mannWhitneyUTest.md), [manova](m/manova.md),
  [norm](n/norm.md)/[normal](n/normal.md), [rand](r/rand.md), [randBeta](r/randBeta.md), [randBinomial](r/randBinomial.md), [randChiSquare](r/randChiSquare.md), [randDiscrete](r/randDiscrete.md), [randExp](r/randExp.md), [randF](r/randF.md), [randGamma](r/randGamma.md), [randLogistic](r/randLogistic.md),
  [randMultivariateNormal](r/randMultivariateNormal.md), [randNormal](r/randNormal.md), [randPoisson](r/randPoisson.md),
  [randStudent](r/randStudent.md), [randUniform](r/randUniform.md), [randWeibull](r/randWeibull.md), [seasonalEsd](s/seasonalEsd.md), [shapiroTest](s/shapiroTest.md), [tTest](t/tTest.md), [zTest](z/zTest.md)
* **数据处理：**[all](a/all.md), [any](a/any.md), [asis](a/asIs.md), [asof](a/asof.md), [bucketCount](b/bucketCount.md), [coevent](c/coevent.md), [cols](c/cols.md), [deepCopy](d/deepCopy.md), [copy](c/copy.md),
  [contextCount](c/contextCount.md), [countNanInf](c/countNanInf.md), [cumPositiveStreak](c/cumPositiveStreak.md), [deltas](d/deltas.md), [dictUpdate!](d/dictUpdate_.md),[distinct](d/distinct.md), [dynamicGroupCumcount](d/dynamicGroupCumcount.md), [dynamicGroupCumsum](d/dynamicGroupCumsum.md), [hashBucket](h/hashBucket.md), [iif](i/iif.md), [imaxLast](i/imaxlast.md), [iminLast](i/iminlast.md), [isDuplicated](i/isDuplicated.md),[keys](k/keys.md), [linearTimeTrend](l/linearTimeTrend.md), [lowerBound](l/lowerbound.md), [lowRange](l/lowRange.md), [mask](m/mask.md), [maxPositiveStreak](m/maxPositiveStreak.md), [mimaxLast](m/mimaxlast.md), [miminLast](m/miminlast.md), [mmaxPositiveStreak](m/mmaxPositiveStreak.md), [pca](p/pca.md), [ratios](r/ratios.md),
  [resample](r/resample.md), [rowImaxLast](r/rowimaxlast.md), [rowIminLast](r/rowiminlast.md), [rows](r/rows.md), [sessionWindow](s/sessionWindow.md),
  [shape](s/shape.md), [size](s/size.md), [stl](s/stl.md), [sumbars](s/sumbars.md), [talibNull](t/talibNull.md), [tmove](t/tmove.md), [topRange](t/topRange.md), [valueChanged](v/valueChanged.md), [values](v/values.md), [winsorize!](w/winsorize_.md), [winsorize](w/winsorize.md), [zscore](z/zscore.md), [differentialEvolution](d/differentialevolution.md)
* **插值:**
  [cubicSpline](c/cubicspline.md), [cubicSplinePredict](c/cubicsplinepredic.md), [dividedDifference](d/dividedDifference.md), [kroghInterpolate](k/kroghinterpolate.md), [loess](l/loess.md), [neville](n/neville.md), [pchipInterpolateFit](p/pchipInterpolateFit.md), [spline](s/spline.md),
  [splrep](s/splrep.md), [splev](s/splev.md)
* **优化：**[brute](b/brute.md),
  [brentq](b/brentq.md), [fmin](f/fmin.md), [fminBFGS](f/fminbfgs.md), [fminLBFGSB](f/fminlbfgsb.md),
  [fminNCG](f/fminncg.md), [fminSLSQP](f/fminslsqp.md), [linprog](l/linprog.md), [osqp](o/osqp.md), [qclp](q/qclp.md), [quadprog](q/quadprog.md), [scs](s/scs.md), [solve](s/solve.md), [socp](s/socp.md)
* **金融分析：**[amortizingFixedRateBondDirtyPrice](a/amortizingfixedratebonddirtyprice.md), [arima](a/arima.md), [bondAccrInt](b/bondaccrint.md), [bondCalculator](b/bondCalculator.md), [bondConvexity](b/bondconvexity.md), [bondDirtyPrice](b/bondDirtyPrice.md), [bondDuration](b/bondDuration.md), [nss](n/nss.md), [ns](n/ns.md), [condValueAtRisk](c/cvar.md), [convertibleFixedRateBondDirtyPrice](c/convertiblefixedratebonddirtyprice.md), [nssPredict](n/nsspredict.md), [trueRange](t/trueRange.md), [valueAtRisk](v/var_0.md), [irs](i/irs.md), [varma](v/varma.md), [bondCashflow](b/bondCashflow.md), [bondYield](b/bondyield.md), [createPricingEngine](c/createpricingengine.md), [floatingRateBondDirtyPrice](f/floatingratebonddirtyprice.md), [treasuryConversionFactor](t/treasuryconversionfactor.md), [crmwCBond](c/crmwcbond.md), [cds](c/cds.md), [vanillaOption](v/vanillaoption.md), [maxDrawdown](m/maxdrawdown.md), [mdd](m/mdd.md), [cummdd](c/cummdd.md), [createYieldCurveEngine](c/createyieldcurveengine.md), [appendForPrediction](a/appendforprediction.md)

## 运算符

* **逻辑：**[and](a/and.md), [bitAnd](b/bitAnd.md), [bitOr](b/bitOr.md), [bitXor](b/bitXor.md), [not](n/not.md),
  [or](o/or.md), [xor](x/xor.md)
* **关系：**[between](b/between.md), [eq](e/eq.md), [eqFloat](e/eqFloat.md), [eqObj](e/eqObj.md), [eqPercent](e/eqpercent.md), [ge](g/ge.md), [gt](g/gt.md), [in](i/in.md), [le](l/le.md), [lt](l/lt.md), [ne](n/ne.md)

## 流数据

* **流表操作：**[appendForJoin](a/appendForJoin.md), [appendMsg](a/appendMsg.md), [clearTablePersistence](c/clearTablePersistence.md), [disableTablePersistence](d/disableTablePersistence.md),
  [dropStreamTable](d/dropStreamTable.md), [enableTableCachePurge](e/enabletablecachepurge.md), [enableTablePersistence](e/enableTablePersistence.md),
  [enableTableShareAndCachePurge](e/enabletableshareandcachepurge.md), [enableTableShareAndPersistence](e/enableTableShareAndPersistence.md), [existsStreamTable](e/existsStreamTable.md), [existsSubscriptionTopic](e/existsSubscriptionTopic.md),
  [getStreamTables](g/getstreamtables.md), [haStreamTable](h/haStreamTable.md), [keyedStreamTable](k/keyedStreamTable.md), [removeTopicOffset](r/removeTopicOffset.md), [setStreamTableFilterColumn](s/setStreamTableFilterColumn.md), [setStreamTableTimestamp](s/setstreamtabletimestamp.md), [share](../progr/statements/share.md), [subscribeTable](s/subscribeTable.md), [unsubscribeTable](u/unsubscribeTable.md), [streamTable](s/streamTable.md)
* **计算引擎：**[createAnomalyDetectionEngine](c/createAnomalyDetectionEngine.md), [createAsofJoinEngine](c/createAsofJoinEngine.md), [createCrossSectionalEngine](c/createCrossSectionalEngine.md), [createDailyTimeSeriesEngine](c/createDailyTimeSeriesEngine.md), [createDualOwnershipReactiveStateEngine](c/createDualOwnershipReactiveStateEngine.md), [createEquiJoinEngine](c/createEquiJoinEngine.md)/ [createEqualJoinEngine](c/createEqualJoinEngine.md), [createLeftSemiJoinEngine](c/createLeftSemiJoinEngine.md),
  [createLookupJoinEngine](c/createLookupJoinEngine.md), [createNarrowReactiveStateEngine](c/createnarrowreactivestateengine.md), [createOrderBookSnapshotEngine](c/createorderbooksnapshotengine.md), [createReactiveStateEngine](c/createReactiveStateEngine.md), [createRuleEngine](c/createRuleEngine.md), [createSessionWindowEngine](c/createSessionWindowEngine.md), [createSnapshotJoinEngine](c/createsnapshotjoinengine.md), [createTimeBucketEngine](c/createtimebucketengine.md), [createTimeSeriesEngine](c/createTimeSeriesEngine.md),
  [createWindowJoinEngine](c/createWindowJoinEngine.md), [streamEngineParser](s/streamEngineParser.md), [createCryptoOrderBookEngine](c/createcryptoorderbookengine.md)
* **工具函数：**[addMetrics](a/addMetrics.md), [addReactiveMetrics](a/addreactivemetrics.md), [conditionalIterate](c/conditionalIterate.md), [dropStreamEngine](d/dropStreamEngine.md)/ [dropAggregator](d/dropAggregator.md), [getComputeNodeCacheWarmupJobStatus](g/getcomputenodecachewarmupjobstatus.md), [getLeftStream](g/getLeftStream.md)/[getRightStream](g/getRightStream.md), [getPersistenceMeta](g/getPersistenceMeta.md), [getReactiveMetrics](g/getreactivemetrics.md), [getSnapshotMsgId](g/getSnapshotMsgId.md), [getStreamEngine](g/getStreamEngine.md)/[getAggregator](g/getAggregator.md), [getStreamEngineList](g/getstreamenginelist.md), [getStreamEngineStat](g/getStreamEngineStat.md)/[getAggregatorStat](g/getAggregatorStat.md), [getRules](g/getrules.md), [getStreamingLeader](g/getStreamingLeader.md), [getStreamingRaftGroups](g/getStreamingRaftGroups.md), [getStreamingStat](g/getStreamingStat.md), [getStreamTableCacheOffset](g/getstreamtablecacheoffset.md), [getStreamTableFilterColumn](g/getStreamTableFilterColumn.md), [getSubscriptionTopic](g/getSubscriptionTopic.md), [getTopicProcessedOffset](g/getTopicProcessedOffset.md),
  [stateIterate](s/stateIterate.md), [warmupComputeNodeCache](w/warmupcomputenodecache.md),
  [warmupStreamEngine](w/warmupStreamEngine.md)

## 元编程

[binaryExpr](b/binaryExpr.md), [eval](e/eval.md), [expr](e/expr.md), [funcByName](f/funcByName.md), [makeCall](m/makeCall.md), [makeUnifiedCall](m/makeUnifiedCall.md), [parseExpr](p/parseExpr.md), [sql](s/sql.md), [sqlCol](s/sqlCol.md),
[sqlColAlias](s/sqlColAlias.md), [sqlDelete](s/sqlDelete.md), [sqlUpdate](s/sqlUpdate.md), [unifiedExpr](u/unifiedExpr.md)

## 高阶函数

[accumulate (:A)](ho_funcs/accumulate.md),
[aggrTopN](ho_funcs/aggrTopN.md), [all](ho_funcs/all.md), [any](ho_funcs/any.md), [byColumn (:V)](ho_funcs/byColumn.md), [byRow (:H)](ho_funcs/byRow.md), [call](ho_funcs/call.md), [compose](c/compose.md), [contextby (:X)](ho_funcs/contextby.md), [cross (:C)](ho_funcs/cross.md)/[pcross](ho_funcs/pcross.md), [each (:E)](ho_funcs/each.md), [eachLeft (:L)](ho_funcs/eachLeft.md),
[eachPost (:O)](ho_funcs/eachPost.md), [eachPre (:P)](ho_funcs/eachPre.md), [eachRight (:R)](ho_funcs/eachRight.md), [groupby (:G)](ho_funcs/groupby.md), [loop (:U)](ho_funcs/loop.md) / [ploop](ho_funcs/ploop.md), [moving](ho_funcs/moving.md), [nullCompare](ho_funcs/nullCompare.md),
[pcall](ho_funcs/pcall.md), [pivot](ho_funcs/pivot.md), [reduce (:T)](ho_funcs/reduce.md), [rolling](ho_funcs/rolling.md),
[rowGroupby](ho_funcs/rowgroupby.md), [segmentby](ho_funcs/segmentby.md), [talib](ho_funcs/talib.md), [tmoving](ho_funcs/tmoving.md), [twindow](ho_funcs/twindow.md), [unifiedCall](ho_funcs/unifiedCall.md), [window](ho_funcs/window.md), [withNullFill](ho_funcs/withNullFill.md)

## 权限与安全

[addAccessControl](a/addAccessControl.md),
[addGroupMember](a/addGroupMember.md), [backupSettings](b/backupsettings.md), [changePwd](c/changePwd.md), [createGroup](c/createGroup.md), [createUser](c/createUser.md), [deleteGroup](d/deleteGroup.md), [deleteGroupMember](d/deleteGroupMember.md), [deleteUser](d/deleteUser.md), [deny](d/deny.md), [getAuthenticatedUsers](g/getAuthenticatedUsers.md), [getGroupAccess](g/getGroupAccess.md), [getGroupList](g/getGroupList.md), [getGroupsByUserId](g/getGroupsByUserId.md), [getUserAccess](g/getUserAccess.md), [getUsersByGroupId](g/getUsersByGroupId.md), [getUserList](g/getUserList.md), [getUserLockedStatus](g/getUserLockedStatus.md), [getUserPasswordStatus](g/getUserPasswordStatus.md), [grant](g/grant.md), [isLoggedIn](i/isLoggedIn.md), [lockUser](l/lockUser.md), [login](l/login.md), [logout](l/logout.md), [resetPwd](r/resetPwd.md), [restoreSettings](r/restoresettings.md), [revoke](r/revoke.md), [scramClientFinal](s/scramClientFinal.md), [scramClientFirst](s/scramClientFirst.md), [unlockUser](u/unlockUser.md)

## 文件系统

[cleanOutdateLogFiles](c/cleanOutdateLogFiles.md), [close](c/close.md), [exists](e/exists.md), [fflush](f/fflush.md), [file](f/file.md), [files](f/files.md), [loadModel](l/loadModel.md), [mkdir](m/mkdir.md), [read!](r/read_.md),
[readBytes](r/readBytes.md), [readLine](r/readLine.md), [readLines](r/readLines.md), [readLines!](r/readLines_.md), [readObject](r/readObject.md), [readRecord!](r/readRecord_.md),
[rm](r/rm.md), [rmdir](r/rmdir.md),
[saveAsNpy](s/saveAsNpy.md), [saveModel](s/saveModel.md), [saveText](s/saveText.md), [saveTextFile](s/saveTextFile.md),
[seek](s/seek.md), [write](w/write.md), [writeBytes](w/writeBytes.md), [writeLine](w/writeLine.md), [writeLines](w/writeLines.md), [writeLog](w/writeLog.md), [writeLogLevel](w/writeloglevel.md), [writeObject](w/writeObject.md), [writeRecord](w/writeRecord.md)

## 系统管理

[cancelConsoleJob](c/cancelConsoleJob.md), [cancelJob](c/cancelJob.md), [closeSessions](c/closeSessions.md), [defined](d/defined.md), [defs](d/defs.md), [deleteScheduledJob](d/deleteScheduledJob.md), [disableResourceTracking](d/disableresourcetracking.md),
[dumpHeapSample](d/dumpheapsample.md), [enableResourceTracking](e/enableresourcetracking.md),
[evalTimer](e/evalTimer.md), [getAclAuditlog](g/getaclauditlog.md), [getAuditLog](g/getauditlog.md), [getClusterPerf](g/getClusterPerf.md), [getConsoleJobs](g/getConsoleJobs.md), [getCurrentSessionAndUser](g/getCurrentSessionAndUser.md), [getDatanodeRestartInterval](g/getDatanodeRestartInterval.md),
[getDynamicConfig](g/getdynamicconfig.md), [getJobMessage](g/getJobMessage.md), [getJobReturn](g/getJobReturn.md), [getJobStat](g/getJobStat.md), [getJobStatus](g/getJobStatus.md), [getLicenseExpiration](g/getLicenseExpiration.md), [getMachineFingerprint](g/getMachineFingerprint.md), [getMemLimitOfAllTempResults](g/getmemlimitofalltempresults.md), [getPerf](g/getPerf.md),
[getRecentJobs](g/getRecentJobs.md), [getScheduledJobs](g/getScheduledJobs.md), [getSessionMemoryStat](g/getSessionMemoryStat.md), [getSupportBundle](g/getSupportBundle.md), [getTSDBDataStat](g/gettsdbdatastat.md), [getTSDBTableIndexCacheStatus](g/gettsdbtableindexcachestatus.md), [getUserHardwareUsage](g/getUserHardwareUsage.md), [getUserTableAccessRecords](g/getUserTableAccessRecords.md), [imtForceGCRedolog](i/imtForceGCRedolog.md), [imtUpdateChunkVersionOnDataNode](i/imtUpdateChunkVersionOnDataNode.md), [installPlugin](i/installPlugin.md), [license](l/license.md), [listRemotePlugins](l/listRemotePlugins.md), [loadModule](l/loadModule.md), [loadModuleFromScript](l/loadmodulefromscript.md), [loadPlugin](l/loadPlugin.md), [member](m/member.md), [module](../progr/statements/module.md),
[objByName](o/objByName.md), [objs](o/objs.md), [partial](p/partial.md), [pipeline](p/pipeline.md), [refCount](r/refCount.md), [saveModule](s/saveModule.md), [scheduleJob](s/scheduleJob.md), [setDatanodeRestartInterval](s/setDatanodeRestartInterval.md), [setDynamicConfig](s/setdynamicconfig.md), [setLogLevel](s/setLogLevel.md), [setMaxJobParallelism](s/setMaxJobParallelism.md), [setMaxJobPriority](s/setMaxJobPriority.md), [setMemLimitOfAllTempResults](s/setmemlimitofalltempresults.md), [setRandomSeed](s/setRandomSeed.md), [setRetentionPolicy](s/setRetentionPolicy.md), [setSystem](s/setSystem.md),
[startHeapSample](s/startheapsample.md),[stopHeapSample](s/stopheapsample.md),
[submitJob](s/submitJob.md), [submitJobEx](s/submitJobEx.md), [submitJobEx2](s/submitJobEx2.md), [syntax](s/syntax.md),
[timer](../progr/statements/timer.md), [undef](u/undef.md), [updateLicense](u/updateLicense.md), [use](../progr/statements/use.md),
[version](v/version.md), [getLoadedPlugins](g/getloadedplugins.md)

## 环境

[clearAllCache](c/clearAllCache.md), [clearCachedModules](c/clearCachedModules.md), [getDiskIOStat](g/getDiskIOStat.md), [getEnv](g/getEnv.md), [getHomeDir](g/getHomeDir.md), [getMemoryStat](g/getMemoryStat.md), [getOS](g/getOS.md), [getOSBit](g/getOSBit.md), [getSystemCpuUsage](g/getSystemCpuUsage.md), [getSystemLoadAvg](g/getSystemLoadAvg.md), [mem](m/mem.md), [moveHotDataToColdVolume](m/moveHotDataToColdVolume.md), [shell](s/shell.md),
[sleep](s/sleep.md), [clearAllIOTDBStaticTableCache](c/clearalliotdbstatictablecache.md), [clearAllIOTDBLatestKeyCache](c/clearalliotdblatestkeycache.md)

## 其它

[attributeNames](a/attributenames.md),
[attributeValues](a/attributevalues.md), ,[constantDesc](c/constantdesc.md), [convertExcelFormula](c/convertExcelFormula.md), [hmac](h/hmac.md), [genericStateIterate](g/genericStateIterate.md), [genericTStateIterate](g/genericTStateIterate.md), [objectChecksum](o/objectChecksum.md), [plot](p/plot.md), [plotHist](p/plotHist.md), [snippet](s/sinppet.md)

