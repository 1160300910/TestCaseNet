<template>
  <!--div class="table-head-css">
    <table ref="middle-table">
      <thead class="thead-middle">
        <tr>
          <th
            v-for="colConfig in colConfigs"
            :key="colConfig.prop"
            :property="colConfig.prop"
            :label="colConfig.label"
            :width="colConfig.width"
          >
            {{ colConfig.label }}
          </th>
        </tr>
      </thead>
    </table>
  </div-->

  <div class="table-contain-css">
    <my-table
      :data="tableData"
      :col-configs="colConfigs"
      highlight-current-row
      border
      ref="table"
      @cell-dblclick="ChangeInfoByCell"
      @current-change="CurrentTableLineChange"
    >
      <template #opt="scope">
        <el-row>
          <el-button
            size="mini"
            type="primary"
            icon="el-icon-edit"
            v-if="!scope.data.row.isRowEditing"
            circle
            @click="ChangeTestCaseTableEditable(scope.data.row)"
          ></el-button>
          <el-button
            v-else
            size="mini"
            type="success"
            icon="el-icon-circle-check"
            circle
            @click="SaveChange(scope.data.row)"
          ></el-button>
          <el-button
            type="info"
            icon="el-icon-picture-outline"
            circle
            size="mini"
          ></el-button
          ><el-button
            v-if="scope.data.row.isRowEditing"
            type="warning"
            size="mini"
            icon="el-icon-error"
            circle
            @click="CancelEditingTestCase(scope.data.row)"
          ></el-button>
          <el-button
            v-else
            type="danger"
            size="mini"
            icon="el-icon-delete"
            circle
            @click="DeleteTableTestcase(scope.data.row)"
          ></el-button>
        </el-row>
      </template>

      <!--template #chooseLevel="scope">
      <el-select v-model="scope.data.row.test_level" placeholder="P0">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
    </template-->
    </my-table>
  </div>
</template>

<script>
import myTable from "./my-table.vue";
const EdibleInput = {
  props: ["row", "column_name", "isColumnEditing", "isRowEditing"],
  template: `
      <el-input type="textarea" v-if="isColumnEditing || isRowEditing" v-model="row[column_name]"
           @input="changeTableCellInput(row, column_name)"
           @blur="blurClickFinishInput(row, column_name)"
           @keyup.enter="
            blurClickFinishInput(row, column_name)
          ">
      </el-input>
      <span v-else-if="column_name=='caseName'" class="custom-table-row"><span> {{ row[column_name]}}</span></span>
   <span v-else ><span> {{ row[column_name]}}</span></span>
   `,
  methods: {
    /**
     * 修改输入时触发
     * 1.如果修改对象为用例名，同步修改左侧导航节点的用例名
     */
    changeTableCellInput(row, column_name) {
      //console.log("====================changeTableCellInput==========================");
      //console.log(column_name);
      if (column_name == "caseName") {
        //只有修改对象为用例名时，触发同步修改
        this.$bus.emit("CASE_NAME_TABLE_CHANGE", {
          value: row.caseName,
          rowId: row.caseId,
        }); //告诉treeNode，发生了用例标题修改事件
      }
    },
    /**
     * 完成输入
     * 1.当输入enter键或者鼠标聚焦到其他的地方时，触发保存
     * 2.将被修改列的数据保存到服务器
     */
    blurClickFinishInput(row, column_name) {
      //console.log(column_name);
      console.log(
        "row[column_name] : " + column_name + "  -----   " + row[column_name]
      );
      this.saveColumnData(row, column_name); //保存到服务器
      row.isColumnEditing[column_name] = false;
    },
    /**
     * 保存当前列的数据到服务器
     * row：当前行
     * column：当前列
     * column_name：当前列名
     */
    saveColumnData(row, column_name) {
      console.log("_______saveColumnData_____________");
      console.log(row.caseId);
      console.log(row[column_name]);
      axios
        .post("updateTableColumnDataByName", {
          caseId: row.caseId,
          column_data: row[column_name],
          column_name: column_name,
        })
        .then((res) => {
          console.log(res.data);
        });
    },
  },
};

const SelectInput = {
  props: ["row", "column_name", "isColumnEditing", "isRowEditing", "options"],
  template: `
      <el-select v-if="isColumnEditing || isRowEditing" v-model="row[column_name]"
          @change="changeSelectTableCell(row, column_name)"
          @focus="focusTableCell(row, column_name)">
      <el-option
          v-for="item in options[column_name]"
          :key="item.key"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
      <span v-else><span> {{ row[column_name]}}</span></span>
    `,
  methods: {
    /**
     * 触发了聚焦输入事件
     */
    focusTableCell(row, column_name) {
      console.log("===============focusTableCell===============");
      console.log(row);
      console.log(column_name);
    },
    /**
     * 修改选中的表格内容
     */
    changeSelectTableCell(row, column_name) {
      //console.log("=============== changeSelectTableCell  ===============");
      //console.log(row[column_name]);
      //console.log(column_name);
      this.saveColumnData(row, column_name); //保存到服务器
      row.isColumnEditing[column_name] = false;
    },
    /**
     * 保存当前列的数据到服务器
     * row：当前行
     * column：当前列
     * column_name：当前列名
     */
    saveColumnData(row, column_name) {
      //console.log("_______saveColumnData_____________");
      //console.log(row.caseId);
      //console.log(row[column_name]);
      axios
        .post("updateTableColumnDataByName", {
          caseId: row.caseId,
          column_data: row[column_name],
          column_name: column_name,
        })
        .then((res) => {
          //console.log(res.data);
        });
    },
  },
};

import axios from "axios";
export default {

  props: ["offsetTop"],
  inject: ["parentObj"],
  watch: {
    currentRow(row) {
      if (row) {
        console.log(this.$refs["table"]);
        this.$refs["table"].ChangeCurrentRow(row);
      } else {
        //this.$refs["table"].setCurrentRow(null);
      }
    },
  },
  created() {
    for (var i = 0; i < this.colConfigs.length; i++) {
      this.compare += this.colConfigs[i].width;
      //th_tree_doms[i].clientWidth = th_doms[i].clientWidth
    }
    //console.log(this.tableData)
    //console.log(this.parentObj.table_datas)
    //this.tableData = this.parentObj.table_datas
  },
  computed: {},
  mounted() {
    const that = this;
    window.onresize = () => {
      return (() => {
        console.log(document.querySelector(".table-head-css"));
        console.log(document.querySelectorAll(".table-head-css th"));
        var th_doms = document.querySelectorAll(".table-head-css th");
        var th_tree_doms = document.querySelectorAll(".has-gutter tr th");
        console.log(th_tree_doms);
        for (var i = 0; i < th_doms.length; i++) {
          this.colConfigs[i].width = th_doms[i].clientWidth;
          //th_tree_doms[i].clientWidth = th_doms[i].clientWidth
        }
        window.screenWidth = document.body.clientWidth;
        that.screenWidth = window.screenWidth;
      })();
    };
    //在组件B中监听动作的发生
    this.$bus.on("CHANGE_TESTCASE_BY_POP", (param) => {
      console.log("CHANGE_TESTCASE_BY_POP 发生了");
      this.ChangeTestCaseTableEditable(param.data);
    });
    /***
     * 接受Tree组件的通知，保存table数据到服务器
     */
    this.$bus.on("SAVE_TESTCASE_TABLE_DATA", (param) => {
      console.log("SAVE_TESTCASE_TABLE_DATA");
      this.saveTableData(param.data, param.fatherId);
    });
    /**
     * 告诉table,
     * 创建了一个新的测试用例行
     * 传入节点数据（）
     */
    this.$bus.on("CREATE_NEW_TESTCASE_NOTIFY_TABLE", (param) => {
      console.log("CREATE_NEW_TESTCASE_NOTIFY_TABLE 发生了");
      this.CreateDefaultTestCaseLine(param.data, param.fatherId, param.broId);
    });
    /***
     * 告诉table,
     * 导航栏选中了新的测试用例行（文件类型）
     * 需要高亮对应行
     */
    this.$bus.on("UPDATE_CURRENT_NODE_DATA_CHOOSE", (data) => {
      console.log("UPDATE_CURRENT_NODE_DATA_CHOOSE 发生了");
      //console.log(data)

      var currentRow = this.FindCurrentRow(data.caseId);
      //console.log(this.$refs["table"]);
      var index = -1;
      if (currentRow) {
        this.$refs["table"].ChangeCurrentRow(currentRow);
        index = this.FindTableIndexByCaseId(data.caseId, data.caseName);
        console.log(
          "???_____________________index_____________________ " + index
        );
        if (index != -1) {
          this.scrollTableTo("table", index);
        }
      } else {
        //alert("Error !!! 没有找到对应的caseId的tableline");
        //需要利用fatherId获取选中testcase的父节点，得到对应的测试用例表
        this.$bus.emit("UPDATE_FATHER_TABLE_DATAS", {
          fatherId: data.fatherId,
          caseId: data.caseId,
        });
        this.waitForTableData(
          () => {
            //函数触发回调，表明table的数据已经更新且载入，可以被读取到
            console.log("action___result");
            index = this.FindTableIndexByCaseId(data.caseId, data.caseName);
            var currentRow = this.FindCurrentRow(data.caseId);
            this.$refs["table"].ChangeCurrentRow(currentRow); //修改当前行 为对应行
            this.scrollTableTo("table", index); //设置滑动的滚轮，滚动到对应的table图表 位置
          },
          500, //设置等待时间间隔为0.5秒
          data.caseId,
          data.caseName
        );
      }
    });

    /***
     * 在table里创建一行
     */
    this.$bus.on("CREATE_NEW_TABLE_POP", (data) => {
      console.log("CREATE_NEW_TABLE_POP 发生了");
    });
    /***
     * 在当前展示的数据table里传入新数据
     */
    this.$bus.on("UPDATE_CURRENT_FOLDER_TABLEDATAS", (param) => {
      console.log("UPDATE_CURRENT_FOLDER_TABLEDATAS 发生了");
      var data = this.SettleCellStates(param.data);
      this.tableData = data;
      //console.log(param);
      if (param.caseId) {
        //如果有当前选中用例，则选中该用例
        var currentRow = this.FindCurrentRow(param.caseId);
        this.$refs["table"].ChangeCurrentRow(currentRow);
      }
    });

    /*
     * 监听页面滚动事件，获取table对象的DOM
     */
    //window.addEventListener("scroll", this.scrollHandle, true);
  },
  methods: {
    /**
     * 处理滑动事件
     */
    scrollHandle() {
      console.log("scrollHandle+++++++++++++++++++++++++");
      var refName = "table";
      if (!refName || !this.$refs[refName]) return;
      let vmEl = this.$refs[refName].$el;
      if (!vmEl) return;

      //console.log(vmEl);
      
      const containerTop = document.querySelectorAll(".el-table__body tbody")[0].scrollTop; // 空间距离顶部的距离
      console.log(document.querySelector(".el-table__body-wrapper").scrollTop);
      console.log(containerTop);
      console.log(this.$refs.table.$el)

      /*
      this.clientRect.top = Math.floor(top - parseInt(this.offsetTop, 10));
      const containerTop = document.querySelector(".main").scrollTop; // 空间距离顶部的距离
      console.log(containerTop);
      this.theadStyle = "top:" + containerTop + "px;";

      refName = "middle-table";
      console.log("this.$refs['middle-table']");
      console.log(this.$refs["middle-table"]);
      if (!refName || !this.$refs[refName]) return;
      vmEl = this.$refs[refName].$el;
      if (!vmEl) return;
      var dom = vmEl.querySelectorAll(".thead-middle")[0]; //获取表头dom

      console.log(dom[0]);
      */

      /*
      var dom = vmEl.querySelectorAll(".el-table__header-wrapper")[0]; //获取表头dom
      var dom_table = vmEl.querySelectorAll(".el-table__body")[0]; //获取表体dom
      var targetOffsetTop = dom.getBoundingClientRect().top; //表头到顶部的距离
      var targetOffsetTop_body = dom_table.getBoundingClientRect().top; //表头到顶部的距离

      const containerTop = document.querySelector(".main").scrollTop; // 空间距离顶部的距离


      const { top } = dom_table.getBoundingClientRect()

      console.log(dom);
      console.log(dom_table);
      console.log(this.offsetTop);
       this.clientRect.top = Math.floor(top - parseInt(this.offsetTop, 10))
      */
      /*
      var trans = targetOffsetTop_body - this.offsetTop;
      console.log(targetOffsetTop, containerTop, this.offsetTop, trans);
      if (trans < 0) {
        //当位移小于0，也就是top已经在屏幕最上面时，进行修正
        dom.style.top = `${containerTop + this.offsetTop}px`;
        dom.style.position = `absolute`;
        dom.style.transform = `translate3d(0px, ${containerTop +
          this.offsetTop}px, 100px)`;
      }*/
    },

    /**
     * 等待通过table的Node所在的fatherID文件夹，
     * 获取该文件夹下全部的测试用例文件
     */
    waitForTableData(callback, interval, caseId, caseName) {
      let handle = setInterval(() => {
        var index = this.FindTableIndexByCaseId(caseId, caseName);
        if (index >= 0) {
          // index>0 说明对应的文件已经在文件集合里面了，表明已经载入了需要的数据
          clearInterval(handle);
          // 此时可以清除间隔且返回到调用函数（俗称回调函数）
          callback();
        } else {
          console.log("waiting!!!!!!!!!!!!!");
          //否则，一直处于等待数据状态
        }
      }, interval);
    },

    /***
     * 获取当前选中节点的index
     */
    FindTableIndexByCaseId(caseId, caseName) {
      var navContents = document.querySelectorAll(".custom-table-row");
      // 所有锚点元素的 offsetTop
      //console.log("navContents===========================");
      //console.log(navContents);
      var index = 0;
      var save = 0;
      for (var i = 0; i < navContents.length; i++) {
        if (
          caseName.trim() !=
          navContents[i].textContent
            .trim()
            .split(" ")[0]
            .trim()
        ) {
          index += 1;
          //console.log("不相等");
        } else {
          return index;
        }
      }
      return -1;
    },
    /**
     * 点击树结构，使得table的界面跳转到对应的位置
     * @param {refName} table的ref值
     * @param {index} table的索引值
     */
    scrollTableTo(refName, index) {
      ("scrollTableTo++++++++++++++++++=================");
      // 获取目标的 offsetTop
      // css选择器是从 1 开始计数，我们是从 0 开始，所以要 +1
      if (!refName || !this.$refs[refName]) return;
      let vmEl = this.$refs[refName].$el;
      if (!vmEl) return;

      var dom = vmEl.querySelectorAll(".el-table__body tr")[index];
      var targetOffsetTop = dom.getBoundingClientRect().top;
      const containerTop = vmEl
        .querySelector(".el-table__body")
        .getBoundingClientRect().top;
      console.log(
        "containerTop: ",
        containerTop,
        "targetOffsetTop: ",
        targetOffsetTop
      );
      targetOffsetTop = targetOffsetTop - containerTop;
      // 获取当前 offsetTop
      let scrollTop = document.querySelector(".el-table__body-wrapper").scrollTop;
      // 定义一次跳 50 个像素，数字越大跳得越快，但是会有掉帧得感觉，步子迈大了会扯到蛋
      console.log("scrollTop", scrollTop);
      console.log("targetOffsetTop", targetOffsetTop);
      const STEP = 350;
      // 判断是往下滑还是往上滑
      if (scrollTop > targetOffsetTop) {
        // 往上滑
        smoothUp();
      } else {
        // 往下滑
        smoothDown();
      }
      // 定义往下滑函数
      function smoothDown() {
        //console.log("smoothDown");
        // 如果当前 scrollTop 小于 targetOffsetTop 说明视口还没滑到指定位置
        if (scrollTop < targetOffsetTop) {
          // 如果和目标相差距离大于等于 STEP 就跳 STEP
          // 否则直接跳到目标点，目标是为了防止跳过了。
          if (targetOffsetTop - scrollTop >= STEP) {
            scrollTop += STEP;
          } else {
            scrollTop = targetOffsetTop;
          }
          document.querySelector(".el-table__body-wrapper").scrollTop = scrollTop;
          console.log(
            "document.querySelector",
            document.querySelector(".el-table__body-wrapper").scrollTop
          );
          // 关于 requestAnimationFrame 可以自己查一下，在这种场景下，相比 setInterval 性价比更高
          requestAnimationFrame(smoothDown);
        }
      }
      // 定义往上滑函数
      function smoothUp() {
        if (scrollTop > targetOffsetTop) {
          if (scrollTop - targetOffsetTop >= STEP) {
            scrollTop -= STEP;
          } else {
            scrollTop = targetOffsetTop;
          }
          document.querySelector(".el-table__body-wrapper").scrollTop = scrollTop;
          requestAnimationFrame(smoothUp);
        }
      }
    },
    /**
     * 取消编辑测试用例
     * 1.取消编辑态
     * 2.回滚到和数据库保持同步
     * 3.节点标题单独回滚
     */
    CancelEditingTestCase(node_data) {
      console.log(
        "——————————————————————CancelEditingTestCase——————————————————————"
      );
      axios
        .get("getTestCaseInfoByCaseId", {
          params: { caseId: node_data.caseId },
        })
        .then((res) => {
          console.log(res.data.msg);
          var data = this.SettleCellState(res.data.msg);
          var d;
          for (d = 0; d < this.tableData.length; d++) {
            if (node_data.caseId == this.tableData[d].caseId) {
              this.tableData[d] = data;
              this.tableData[d].isRowEditing = false;
              this.$bus.emit("CASE_NAME_TABLE_CHANGE", {
                value: data.caseName,
                rowId: node_data.caseId,
              }); //告诉treeNode，发生了用例标题修改事件；title被修改为旧的值
            }
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    /***
     * 在服务器上创建一个默认测试用例，
     * 并返回该用例的id
     */
    CreateDefaultTestCaseLine(data, fatherId, broCaseId) {
      //console.log(data);
      //console.log(fatherId);
      var newTestCase = {
        caseId: data.caseId,
        caseName: "",
        preCondition: "",
        actionCondition: "",
        type: data.type,
        preResult: "",
        ps: "",
        test_level: "P1",
        changer: this.parentObj.userName,
        fatherId: fatherId,

        isRowEditing: true,
        isColumnEditing: {
          caseName: false,
          preCondition: false,
          preResult: false,
          actionCondition: false,
          ps: false,
          changer: false,
          test_level: false,
        },
      };
      //this.parentObj.table_datas.unshift(newTestCase);
      //this.tableData = this.parentObj.table_datas;
      if (broCaseId) {
        this.insertIntoTableAfterBrother(broCaseId, newTestCase);
      } else {
        this.tableData.push(newTestCase);
      }
      this.$refs["table"].ChangeCurrentRow(newTestCase);
    },
    /***
     * 找到table表里面对应的兄弟用例id，在兄弟的后面插入
     */
    insertIntoTableAfterBrother(broCaseId, newTestCase) {
      for (var i = 0; i < this.tableData.length; i++) {
        if (broCaseId == this.tableData[i].caseId) {
          this.tableData.splice(1, i, newTestCase);
        }
      }
    },
    /***
     * 查找导航栏中选中用例所对应的行
     */
    FindCurrentRow(caseId) {
      var d;
      for (d = 0; d < this.tableData.length; d++) {
        //(this.tableData[d]);
        if (caseId == this.tableData[d].caseId) {
          return this.tableData[d];
        }
      }
      return "";
    },
    /**
     * 保存测试用例的修改到服务器
     * 输入：
     *    data：测试用例的树节点数据,
     *    fatherId：测试用例的父节点
     *
     */
    saveTableData(data, fatherId) {
      // 查找对应的tabel数据
      var table_line = this.FindNodeEdit(data.caseId, this.tableData);
      axios
        .post("saveTestCase", {
          caseId: data.caseId,
          caseName: table_line.caseName,
          preCondition: table_line.preCondition,
          actionCondition: table_line.actionCondition,

          preResult: table_line.preResult,
          ps: table_line.ps,
          test_level: table_line.test_level,
          changer: this.parentObj.userId,

          fatherId: fatherId,
          tag: table_line.tag,
          fileType: "file",
        })
        .then((res) => {
          //console.log(res);
          //是需要修改的行
          table_line.isRowEditing = false;
        });
    },
    /**
     * 保存测试用例的修改到服务器
     * 输入：新建测试用例数据 nodedata
     * 可以用caseId获取对应的树数据中的当前节点的父节点和儿子节点
     *
     */
    SaveChange(node_data) {
      var that = this;
      console.log("_____________SaveChange_______________________");
      //console.log(node_data);
      //console.log(tableData);
      //用例编号，父用例文件夹id，类型（文件夹or用例）
      //用例标题，用例等级,前置条件，执行条件，预期结果，备注，标签，修改人
      var fatherId, data, childrenIds;
      fatherId = node_data.fatherId;
      //alert("fatherId:  " + fatherId);
      // 在table里找找有没有这个tabelId==NodeId的东西
      data = this.FindNodeEdit(node_data.caseId);
      if (data) {
        axios
          .post("saveTestCase", {
            caseId: node_data.caseId,
            caseName: data.caseName,
            preCondition: data.preCondition,
            actionCondition: data.actionCondition,

            preResult: data.preResult,
            ps: data.ps,
            test_level: data.test_level,
            changer: this.parentObj.userId,

            fatherId: fatherId,
            childId: childrenIds,
            tag: data.tag,
            fileType: "file",
          })
          .then((res) => {
            console.log(res);
            //是需要修改的行
            data.isRowEditing = false;
            this.$bus.emit("SAVE_TABLE_ROW", { caseId: node_data.caseId });
          })
          .catch(function(error) {
            console.log(that.parentObj.nowParent.data);
            console.log(childrenIds);
            console.log(data);
            alert("Error " + error);
          });
      }
    },
    /***
     * 从服务器传过来的数据缺少客户端状态
     * 增设客户端里，每个节点的状态标记
     */
    SettleCellStates(datas) {
      for (var i = 0; i < datas.length; i++) {
        datas[i]["isRow"] = false;
        datas[i]["isColumnEditing"] = {
          caseName: false,
          preCondition: false,
          preResult: false,
          actionCondition: false,
          ps: false,
          test_level: false,
          changer: false,
        };
      }
      return datas;
    },
    /***
     * 设置节点的状态
     */
    SettleCellState(data) {
      data["isRow"] = false;
      data["isColumnEditing"] = {
        caseName: false,
        preCondition: false,
        preResult: false,
        actionCondition: false,
        ps: false,
        test_level: false,
        changer: false,
      };

      return data;
    },
    /**
     * 双击table的单个Cell
     * 触发单个内容的修改事件
     */
    ChangeInfoByCell(row, column, cell, event) {
      if (!row.isRowEditing) {
        //当不在整行编辑模式时
        console.log("——————————cellClick—————————");
        console.log(row);
        console.log(column);
        console.log(cell);
        console.log(event);
        row.isColumnEditing[column.property] = true;
        console.log("——————————cellClickActivate—————————");
      }
    },
    /**
     * 修改测试用例，将对应行全部可编辑区域变成可编辑状态
     * colConfigs ：
     * caseId ：需要修改表格的行id
     * tableData ：表格数据
     */
    ChangeTestCaseTableEditable(node_data) {
      console.log(node_data.caseId);
      var data;
      data = this.FindNodeEdit(node_data.caseId);
      if (data) {
        //是需要修改的行
        data.isRowEditing = true;
      }
    },

    /**
     * 切换当前选中的行
     * 输入：当前选中行currentRow；之前的选中行oldCurrentRow
     * 1.保存其他的选中行
     * 2.修改当前的选中TreeNode节点,展开其父节点，并显示选中了对应节点
     * 3.
     */
    CurrentTableLineChange(currentRow, oldCurrentRow) {
      console.log(
        "——————————————————————————CurrentTableLineChange————————————————————————"
      );
      console.log(currentRow);
      console.log(oldCurrentRow);
      if (currentRow && currentRow.caseName) {
        this.SaveOtherTableRows(currentRow);
        this.$bus.emit("CHANGE_CURRENT_TREENODE_FROM_TABLE", {
          caseId: currentRow.caseId,
          caseName: currentRow.caseName,
        });
      }
    },
    /***
     * 保存其他选中行到服务器
     * 输入：
     *     需要保存的行内信息：除了row之外的行,row不能为空
     *
     */
    SaveOtherTableRows(row) {
      var t;
      var table_datas = this.tableData;
      for (t = 0; t < table_datas.length; t++) {
        //console.log("------");
        //console.log(table_datas[t]);
        if (table_datas[t].caseId != row.caseId) {
          if (table_datas[t].isRowEditing) {
            this.SaveChange(row);
          }
        }
      }
    },

    /***
     * ——————————————————————————————————————————————————————————————————————————————————————
     */

    /**
     * 删除测试用例
     * 1.从tableData里面删除
     * 2.TreeNode也需要删除对应数据
     */
    DeleteTableTestcase(table_data) {
      this.$bus.emit("DELETE_TESTCASE_NODE_BYTABLE", {
        data: table_data,
      });
      /*
      console.log("---------------");
      console.log(table_data.caseId);

      axios
        .post("deleteTestCase", {
          caseId: table_data.caseId,
        })
        .then((res) => {
          console.log(res);
        });*/
    },
    /***
     * 从列表里找到对应的id的数据,修改其他id数据为不可编辑状态
     * caseId:对应的用例id
     * tableData:表格数据
     */
    FindNodeEdit(caseId) {
      var tableData = this.tableData;
      var data, save;
      for (data in tableData) {
        data = tableData[data];
        if (caseId == data.caseId) {
          save = data;
        } else {
          data.isRowEditing = false;
        }
      }
      if (save) return save;
      return false;
    },

    Test(data) {
      console.log(data);
    },
  },
  destroy() {
    // 必须移除监听器，不然当该vue组件被销毁了，监听器还在就会出错
    //window.removeEventListener("scroll", this.scrollHandle);
  },
  components: { myTable },
  data() {
    this.compare = 0;
    const tableData = [];
    this.colConfigs = [
      {
        prop: "caseName",
        label: "用例标题",
        width: 200,
        component: EdibleInput,
      },
      {
        prop: "test_level",
        label: "用例等级",
        width: 80,
        component: SelectInput,
      },
      {
        prop: "preCondition",
        label: "前置条件",
        width: 140,
        component: EdibleInput,
      },
      {
        prop: "actionCondition",
        label: "执行条件",
        width: 180,
        component: EdibleInput,
      },
      {
        prop: "preResult",
        label: "预期结果",
        width: 280,
        component: EdibleInput,
      },
      {
        prop: "ps",
        label: "备注",
        width: 180,
        component: EdibleInput,
      },

      {
        prop: "tag",
        label: "标签",
        width: 80,
        chooseble: false,
      },
      { prop: "operate", label: "操作", width: 140, slot: "opt" },
      {
        prop: "changer",
        label: "修改人",
        width: 140,
      },

      // 模版中的元素需要对应的有 slot="opt" 属性
    ];
    return {
      currentRow: "",
      tableData: [], //this.parentObj.table_datas,
    };
  },
};
</script>
<style scoped>
.table-head-css {
  display: flex;
  flex-grow: 1;
  flex-direction: column;
  position: absolute;
  top: 0px;
  left: 0px;
  bottom: 0px;
  right: 0px; /* 距离右边0像素 */
  padding-left: 10px;
  line-height: 40px;
  /* background-color: red; */
}

.table-contain-css {
  display: flex;
  flex-grow: 1;
  flex-direction: column;
  position: absolute;
  top: 00px;
  left: 0px;
  bottom: 10px;
  right: 10px; /* 距离右边0像素 */
  padding-left: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
}
.custom-table-row > span {
}
/*
.thead-middle {
  background: rgb(216, 216, 216);
  color: rgb(32, 32, 32);
  border: 1px solid black;
  text-align: center;
  font-size: 20px;
  font-weight: 500;
  height: 40px;
}

.thead-middle > .tr > .th {
  border: 1px solid black;
}*/
</style>
