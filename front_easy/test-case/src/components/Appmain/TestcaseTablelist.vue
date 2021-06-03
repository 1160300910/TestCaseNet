<template>
  <el-table
  border=true
    :data="tableData"
    style="width: 100%"
    :row-class-name="tableRowClassName">
    <el-table-column
      prop="name"
      label="用例名"
      width="180">
    </el-table-column>
    <el-table-column
      prop="level"
      label="用例等级">
    </el-table-column>
    <el-table-column
      prop="actionmethod"
      label="执行方案"
      width="180">
    </el-table-column>
    <el-table-column
      prop="ps"
      label="备注">
    </el-table-column>
    <el-table-column
      prop="actionResult"
      label="执行结果">
    </el-table-column>
    <el-table-column
      prop="changePeo"
      label="修改人">
    </el-table-column>
    <el-table-column
      prop="changeDate"
      label="修改日期">
    </el-table-column>
  </el-table>
</template>

<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>

<script>
  export default {
    methods: {
      tableRowClassName({ rowIndex}) {
        if (rowIndex === 1) {
          return 'warning-row';
        } else if (rowIndex === 3) {
          return 'success-row';
        }
        return '';
      }
    },
    data() {
      return {
        tableData: [{
          name: '入口-1',
          actionmethod: '点击弹出对应GM命令或者执行方案',
          level: 'P1',
          changeDate:'2021-5-23',
          ps:'备注巴啦啦把',
          actionResult:'成功',
          changePeo:'西子卡'
        }, {
          name: '入口-2',
          actionmethod: '点击弹出对应GM命令或者执行方案',
          level: 'P2'
        }, {
          name: '入口-3',
          actionmethod: '点击弹出对应GM命令或者执行方案',
          level: 'P1',
        }, {
          name: '入口-4',
          actionmethod: '点击弹出对应GM命令或者执行方案',
          level: 'P1'
        }]
      }
    }
  }
</script>